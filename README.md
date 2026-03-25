# PhenixRTS Monitoring System

## ✅ Nova Funcionalidade: Monitor de Saúde em Tempo Real

Agora o sistema monitora **a saúde dos canais ao vivo** usando o endpoint oficial  
`/pcast/channel/<channelId>/publishers/count`

### Como usar

1. Configure seu `.env` (veja `.env.example`)
2. Rode o monitor:

```bash
python channel_health_monitor.py
```
