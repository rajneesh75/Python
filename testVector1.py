import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Input, Dense, Lambda, Layer
from tensorflow.keras.models import Model
from tensorflow.keras import backend as k
from tensorflow.keras import losses
from dotenv import load_dotenv

load_dotenv()


# sampling function
def sampling(args):
    mu, log_var = args
    eps = k.random_normal(shape=(batch_size, z_dim), mean=0., stddev=1.0)
    return mu + k.exp(log_var) * eps


# Custom KL divergence layer
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

print(x_tr.shape, x_te.shape)
print(x_tr_flat.shape, x_te_flat.shape)

# Neural Network Parameters
batch_size, n_epoch = 100, 50
n_hidden, z_dim = 256, 2

plt.imshow(x_tr[1])  # Use 'gray' colormap for grayscale images
plt.title(f"Label: {y_tr[1]}")  # Optional: Show the label as the title
plt.axis('off')  # Optional: Hide axes for better visualization
plt.show()  # Display the image

# Encoder - from 784->256->128->2
inputs_flat = Input(shape=(x_tr_flat.shape[1:]))
x_flat = Dense(n_hidden, activation='relu')(inputs_flat)  # first hidden layer
x_flat = Dense(n_hidden // 2, activation='relu')(x_flat)  # second hidden layer

# hidden state, which we will pass into the Model to get the Encoder.
mu_flat = Dense(z_dim)(x_flat)
log_var_flat = Dense(z_dim)(x_flat)
z_flat = Lambda(sampling, output_shape=(z_dim,))([mu_flat, log_var_flat])

# Decoder - from 2->128->256->784
latent_inputs = Input(shape=(z_dim,))
z_decoder1 = Dense(n_hidden // 2, activation='relu')
z_decoder2 = Dense(n_hidden, activation='relu')
y_decoder = Dense(x_tr_flat.shape[1], activation='sigmoid')
z_decoded = z_decoder1(latent_inputs)
z_decoded = z_decoder2(z_decoded)
y_decoded = y_decoder(z_decoded)
decoder_flat = Model(latent_inputs, y_decoded, name="decoder_conv")

outputs_flat = decoder_flat(z_flat)

# variational autoencoder (VAE) - to reconstruction input
reconstruction_loss = losses.binary_crossentropy(inputs_flat, outputs_flat) * x_tr_flat.shape[1]


kl_loss = KLLossLayer()([mu_flat, log_var_flat])
vae_flat_loss = reconstruction_loss + kl_loss

# Build model
#  Ensure that the reconstructed outputs are as close to the inputs
vae_flat = Model(inputs_flat, outputs_flat)
vae_flat.add_loss(vae_flat_loss)
vae_flat.compile(optimizer='adam')

# train
vae_flat.fit(
    x_tr_flat,
    shuffle=True,
    epochs=n_epoch,
    batch_size=batch_size,
    validation_data=(x_te_flat, None),
    verbose=1
)

# Build encoders
encoder_f = Model(inputs_flat, z_flat)  # flat encoder

# Plot of the digit classes in the latent space
x_te_latent = encoder_f.predict(x_te_flat, batch_size=batch_size,verbose=0)
plt.figure(figsize=(8, 6))
plt.scatter(x_te_latent[:, 0], x_te_latent[:, 1], c=y_te, alpha=0.75)
plt.title('MNIST 2D Embeddings')
plt.colorbar()
plt.show()