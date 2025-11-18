import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Input, Dense, Lambda, Layer
from tensorflow.keras.models import Model
from tensorflow.keras import backend as k
from tensorflow.keras import losses

# Neural Network Parameters
batch_size, n_epoch = 100, 50
n_hidden, z_dim = 256, 2


# Sampling function
def sampling(args):
    mu, log_var = args
    eps = k.random_normal(shape=(k.shape(mu)[0], z_dim), mean=0., stddev=1.0)
    return mu + k.exp(0.5 * log_var) * eps  # Corrected variance scaling


# Custom KL divergence loss layer
class KLLossLayer(Layer):
    def call(self, inputs):
        mu, log_var = inputs
        kl_loss = -0.5 * k.sum(1 + log_var - k.square(mu) - k.exp(log_var), axis=-1)
        return kl_loss


# Load data – training and test
(x_tr, y_tr), (x_te, y_te) = mnist.load_data()

# Normalize and Reshape images (flatten)
x_tr, x_te = x_tr.astype('float32') / 255., x_te.astype('float32') / 255.
x_tr_flat, x_te_flat = x_tr.reshape(x_tr.shape[0], -1), x_te.reshape(x_te.shape[0], -1)

# Encoder - from 784->256->128->2
inputs_flat = Input(shape=(x_tr_flat.shape[1],))
x_flat = Dense(n_hidden, activation='relu')(inputs_flat)
x_flat = Dense(n_hidden // 2, activation='relu')(x_flat)

mu_flat = Dense(z_dim)(x_flat)
log_var_flat = Dense(z_dim)(x_flat)
z_flat = Lambda(sampling)([mu_flat, log_var_flat])

# Decoder - from 2->128->256->784
latent_inputs = Input(shape=(z_dim,))
z_decoder1 = Dense(n_hidden // 2, activation='relu')(latent_inputs)
z_decoder2 = Dense(n_hidden, activation='relu')(z_decoder1)
y_decoded = Dense(x_tr_flat.shape[1], activation='sigmoid')(z_decoder2)

decoder_flat = Model(latent_inputs, y_decoded, name="decoder")
outputs_flat = decoder_flat(z_flat)

# Variational Autoencoder (VAE)
vae_flat = Model(inputs_flat, outputs_flat)

# ✅ Proper loss calculations
reconstruction_loss = tf.reduce_sum(losses.binary_crossentropy(inputs_flat, outputs_flat), axis=-1)
kl_loss = tf.reduce_sum(-0.5 * (1 + log_var_flat - tf.square(mu_flat) - tf.exp(log_var_flat)), axis=-1)

# ✅ Add losses to the model
vae_flat.add_loss(tf.reduce_mean(reconstruction_loss))
vae_flat.add_loss(tf.reduce_mean(kl_loss))

vae_flat.compile(optimizer='adam')

# Train the model
vae_flat.fit(
    x_tr_flat,
    epochs=n_epoch,
    batch_size=batch_size,
    validation_data=(x_te_flat, None),
    verbose=1
)

# Build encoder model
encoder_f = Model(inputs_flat, z_flat)

# Plot digit classes in latent space
x_te_latent = encoder_f.predict(x_te_flat, batch_size=batch_size, verbose=0)

plt.figure(figsize=(8, 6))
plt.scatter(x_te_latent[:, 0], x_te_latent[:, 1], c=y_te, cmap='jet', alpha=0.75)
plt.colorbar()
plt.title('MNIST 2D Embeddings')
plt.xlabel("Latent Dim 1")
plt.ylabel("Latent Dim 2")
plt.show()
