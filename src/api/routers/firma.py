import fitz  # PyMuPDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def load_private_key(private_key_path):
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key

def load_public_key(public_key_path):
    with open(public_key_path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def sign_pdf(pdf_path, signed_pdf_path, private_key_path):
    # Cargar el PDF
    doc = fitz.open(pdf_path)
    
    # Cargar la clave privada
    private_key = load_private_key(private_key_path)

    # Crear un hash del contenido del PDF
    pdf_bytes = doc.tobytes()
    pdf_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pdf_hash.update(pdf_bytes)
    digest = pdf_hash.finalize()

    # Firmar el hash
    signature = private_key.sign(
        digest,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Agregar la firma al PDF
    doc.save(signed_pdf_path, garbage=3, deflate=True, clean=True)

    # Cerrar el documento
    doc.close()

    # Guardar la firma en un archivo separado (puedes cambiar esto según tus necesidades)
    with open(signed_pdf_path.replace('.pdf', '_signature.bin'), 'wb') as sig_file:
        sig_file.write(signature)

def verify_pdf_signature(pdf_path, public_key_path):
    # Cargar el PDF
    doc = fitz.open(pdf_path)

    # Cargar la clave pública
    public_key = load_public_key(public_key_path)

    # Obtener el contenido del PDF
    pdf_bytes = doc.tobytes()
    
    # Crear un hash del contenido del PDF
    pdf_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
    pdf_hash.update(pdf_bytes)
    digest = pdf_hash.finalize()

    # Leer la firma desde el archivo
    signature_file = pdf_path.replace('.pdf', '_signature.bin')
    with open(signature_file, 'rb') as sig_file:
        signature = sig_file.read()

    # Verificar la firma
    try:
        public_key.verify(
            signature,
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        print("La firma es válida.")
    except Exception as e:
        print(f"La firma no es válida: {str(e)}")

    # Cerrar el documento
    doc.close()
