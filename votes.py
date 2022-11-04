import asn1tools
import os

asn1_path = 'lib/bu.asn1'
conv = asn1tools.compile_files(asn1_path)

bu_path = os.environ.get("BU_FILE_PATH")

with open(bu_path, "rb") as file:
  envelope_encoded = bytearray(file.read())

  envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", envelope_encoded)
  bu_encoded = envelope_decoded["conteudo"]
  bu_decoded = conv.decode("EntidadeBoletimUrna", bu_encoded)

  arr = bu_decoded['resultadosVotacaoPorEleicao']
  for a in arr:
    results = a['resultadosVotacao']
    for r in results:
      total_voters = r['qtdComparecimento']
      print(f"Total de Votantes: {total_voters}")
      totals = r['totaisVotosCargo']
      for t in totals:
        if t['codigoCargo'][1] == 'presidente':
          votes = t['votosVotaveis']
          b = 0
          l = 0
          for v in votes:
            if v.get('tipoVoto') == 'nominal':
              print(f"Partido {v['identificacaoVotavel']['partido']}: {v['quantidadeVotos']} ({v['quantidadeVotos'] / total_voters:.2%})")
              if v['identificacaoVotavel']['partido'] == 22: b += v['quantidadeVotos']
              else: l += v['quantidadeVotos']
            elif v.get('tipoVoto') == 'branco':
              print(f"Brancos: {v['quantidadeVotos']} ({v['quantidadeVotos'] / total_voters:.2%})")
            elif v.get('tipoVoto') == 'nulo':
              print(f"Nulo: {v['quantidadeVotos']} ({v['quantidadeVotos'] / total_voters:.2%})")
          
          print(f"Votos Válidos: L {l / (b + l):.2%} x B: {b / (b + l):.2%}")
  