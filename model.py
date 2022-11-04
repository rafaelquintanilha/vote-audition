import asn1tools
import os

asn1_path = 'lib/assinatura.asn1'
conv = asn1tools.compile_files(asn1_path)

vscmr_path = os.environ.get("VSCMR_FILE_PATH")

with open(vscmr_path, "rb") as file:
  envelope_encoded = bytearray(file.read())

  envelope_decoded = conv.decode("EntidadeAssinaturaResultado", envelope_encoded)

  print(f"Modelo Urna: {envelope_decoded['modeloUrna']}")