# Gerador de QRCodes

Projeto em **Python (Pillow + Treepoem)** dentro de **Docker**, para gerar códigos **Aztec** numerados com logo central e rótulo abaixo.

---

## 🧩 Estrutura

```
📂 app/
│   ├── assets/logo.png
│   ├── generate.py
│   ├── requirements.txt
│   └── output/           ← imagens geradas aqui
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md

```

---

## 🐋 Como rodar

```bash
docker compose up --build
```

Os QRCodes gerados aparecerão em `app/output/`.

---

## ⚙️ Personalização

Edite as variáveis de ambiente no `docker-compose.yml`:

| Variável | Descrição | Exemplo |
|-----------|------------|----------|
| `COUNT` | Quantidade de códigos a gerar | `64` |
| `PREFIX` | Prefixo do rótulo abaixo | `"MESA - "` |
| `ZERO_PAD` | Dígitos para padding | `2` |
| `FG_COLOR` | Cor do código (hex) | `#000000` |
| `BG_COLOR` | Cor de fundo | `#ffffff` |
| `LABEL_COLOR` | Cor do texto | `#000000` |
| `LOGO_SCALE` | Proporção do logo central | `0.24` |
| `IMAGE_SIZE` | Tamanho final do QR (px) | `800` |

---

## 🧾 Requisitos

- Docker Compose moderno (sem `version:`)
- Logo PNG em `app/assets/logo.png`
- Pasta `app/output/` criada localmente ou deixada para o container gerar

---

## 📄 Licença
Uso livre para projetos pessoais e corporativos.
