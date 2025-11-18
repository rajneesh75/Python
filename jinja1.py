from jinja2 import Template

template = Template(open('nginx.conf.j2').read())
config = template.render(server_name='example.com', document_root='/var/www/html')
print(config)

with open('example.conf', 'w') as f:
    f.write(config)

print("✅ Configuration file created from template!")
