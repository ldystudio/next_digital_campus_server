from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

try:
    with open("private.pem", "r") as f:
        signing_key = f.read()
    with open("public.pem", "r") as f:
        verifying_key = f.read()
except FileNotFoundError:
    # 生成 RSA 密钥对
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # 将私钥保存到文件
    with open("private.pem", "wb") as f:
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        signing_key = private_pem.decode("utf-8")
        f.write(private_pem)

    # 将公钥保存到文件
    with open("public.pem", "wb") as f:
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        verifying_key = public_pem.decode("utf-8")
        f.write(public_pem)
