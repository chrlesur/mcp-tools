# 🔌 Configurer un serveur MCP dans Cline (VS Code / VSCodium)

> Ce guide explique comment connecter un serveur MCP Cloud Temple à **Cline**
> (extension VS Code / VSCodium) pour que l'agent IA puisse utiliser vos outils.

---

## 1. Prérequis

- **VS Code** ou **VSCodium** avec l'extension **Cline** installée
- Votre serveur MCP lancé (via `docker compose up -d`)
- Un **token d'accès** (bootstrap key ou token S3)

## 2. Où se trouve le fichier de configuration ?

Cline stocke ses serveurs MCP dans un fichier JSON :

| OS | Chemin |
|----|--------|
| **macOS** | `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| **macOS (VSCodium)** | `~/Library/Application Support/VSCodium/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| **Linux** | `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| **Linux (VSCodium)** | `~/.config/VSCodium/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json` |
| **Windows** | `%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json` |

> **Astuce** : Dans Cline, cliquez sur l'icône ⚙️ (serveurs MCP) en haut de la sidebar
> pour ouvrir directement ce fichier.

## 3. Configuration — Serveur MCP Streamable HTTP

### 3.1 Configuration minimale

```json
{
  "mcpServers": {
    "mon-mcp-service": {
      "url": "http://localhost:8082/mcp",
      "headers": {
        "Authorization": "Bearer VOTRE_TOKEN_ICI"
      }
    }
  }
}
```

**Explications** :
- `"mon-mcp-service"` — Nom libre, affiché dans Cline
- `"url"` — URL complète du endpoint MCP, **toujours avec `/mcp`** à la fin
- `"headers"` — Le Bearer token pour l'authentification
- Le port `8082` est le port WAF (pas le port interne du service)

### 3.2 Avec la bootstrap key (développement)

```json
{
  "mcpServers": {
    "mcp-tools-dev": {
      "url": "http://localhost:8082/mcp",
      "headers": {
        "Authorization": "Bearer change_me_in_production"
      }
    }
  }
}
```

### 3.3 Avec un token S3 (production)

D'abord, créez un token via la CLI ou la console admin :

```bash
# Via CLI
python scripts/mcp_cli.py --token $ADMIN_BOOTSTRAP_KEY token create cline-dev \
  --permissions read,write

# Ou via la console admin : http://localhost:8082/admin → Tokens → Créer
```

Puis utilisez le token brut retourné :

```json
{
  "mcpServers": {
    "mcp-tools": {
      "url": "http://localhost:8082/mcp",
      "headers": {
        "Authorization": "Bearer mcp_a1b2c3d4e5f6g7h8..."
      }
    }
  }
}
```

### 3.4 Plusieurs serveurs MCP

Vous pouvez connecter **plusieurs serveurs MCP** simultanément :

```json
{
  "mcpServers": {
    "mcp-tools": {
      "url": "http://localhost:8082/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN_TOOLS"
      }
    },
    "mcp-vault": {
      "url": "http://localhost:8083/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN_VAULT"
      }
    },
    "graph-memory": {
      "url": "http://localhost:8084/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN_MEMORY"
      }
    }
  }
}
```

Cline verra tous les outils de tous les serveurs connectés.

## 4. Vérifier la connexion

### Dans Cline

1. Ouvrez la sidebar Cline
2. Cliquez sur l'icône ⚙️ (MCP Servers) en haut
3. Votre serveur doit apparaître avec un **point vert** ✅
4. Cliquez dessus pour voir la liste des outils disponibles

### En cas de problème

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| Point rouge 🔴 | Serveur non accessible | Vérifiez `docker compose ps` et `curl http://localhost:8082/health` |
| Point rouge 🔴 | Token invalide | Vérifiez le token dans le header Authorization |
| Point orange 🟡 | Timeout | Augmentez les timeouts WAF ou vérifiez les logs `docker compose logs waf` |
| Pas de serveur visible | Fichier JSON mal formaté | Vérifiez la syntaxe JSON (virgules, accolades) |
| Outils non listés | Serveur en cours de démarrage | Attendez quelques secondes et rafraîchissez |

### Logs utiles pour le debug

```bash
# Logs du serveur MCP
docker compose logs -f mon-mcp

# Logs du WAF
docker compose logs -f waf

# Health check direct
curl http://localhost:8082/health

# Vérifier les outils disponibles
curl -H "Authorization: Bearer VOTRE_TOKEN" http://localhost:8082/mcp -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## 5. Configuration avancée

### 5.1 Serveur distant (pas localhost)

```json
{
  "mcpServers": {
    "mcp-tools-prod": {
      "url": "https://mcp-tools.mondomaine.com/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN_PROD"
      }
    }
  }
}
```

### 5.2 Désactiver un serveur sans supprimer la config

```json
{
  "mcpServers": {
    "mcp-tools": {
      "disabled": true,
      "url": "http://localhost:8082/mcp",
      "headers": {
        "Authorization": "Bearer TOKEN"
      }
    }
  }
}
```

## 6. Différences SSE vs Streamable HTTP

| | SSE (ancien) | Streamable HTTP (actuel) |
|---|---|---|
| **Endpoint** | `/sse` | `/mcp` |
| **Config Cline** | `"command": "..."` (stdio) ou `"url": ".../sse"` | `"url": ".../mcp"` |
| **Transport** | Server-Sent Events (GET) | HTTP POST + SSE optionnel |
| **Compatibilité** | MCP SDK < 1.8 | MCP SDK ≥ 1.8 |

> **Important** : Tous les serveurs MCP Cloud Temple utilisent **Streamable HTTP**.
> L'endpoint est toujours `/mcp`, jamais `/sse`.

---

*Guide créé le 8 mars 2026 — Starter Kit MCP Cloud Temple*
