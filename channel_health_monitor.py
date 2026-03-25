import os
import time
import logging
from dotenv import load_dotenv
from main import PhenixRTS

load_dotenv()

# Configuração de logging com cores
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)

# Cores para console
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class ChannelHealthMonitor:
    def __init__(self, interval_seconds: int = 8):
        app_id = os.getenv('PHENIXRTS_APP_ID')
        password = os.getenv('PHENIXRTS_PASSWORD')

        if not app_id or not password:
            raise ValueError("❌ PHENIXRTS_APP_ID e PHENIXRTS_PASSWORD não encontrados no .env")

        self.phenix = PhenixRTS(app_id, password)
        self.interval = interval_seconds
        self.channel_cache = {}  # channelId -> name

        logging.info(f"{Colors.BOLD}🚀 PhenixRTS Health Monitor iniciado{Colors.RESET}")

    def load_channels(self):
        """Carrega todos os canais da API"""
        try:
            channels = self.phenix.get_channels()
            self.channel_cache = {ch.get("channelId"): ch.get("name", "Sem nome") for ch in channels}
            
            logging.info(f"{Colors.GREEN}✓ Carregados {len(channels)} canais da API{Colors.RESET}")
            for ch in channels:
                logging.info(f"   • {ch.get('name')} ({ch.get('channelId')})")
            print()
            return True
        except Exception as e:
            logging.error(f"{Colors.RED}✗ Erro ao carregar canais: {e}{Colors.RESET}")
            return False

    def monitor(self):
        if not self.load_channels():
            logging.error("Não foi possível carregar os canais. Encerrando.")
            return

        while True:
            logging.info(f"{Colors.BOLD}🔍 Verificando saúde de {len(self.channel_cache)} canais...{Colors.RESET}")

            for channel_id, name in self.channel_cache.items():
                try:
                    health = self.phenix.get_publishers_count(channel_id)
                    count = health.get("count", 0)
                    status = health.get("status", "unknown")

                    if count > 0:
                        logging.info(f"{Colors.GREEN}✅ {name} | {count} publisher(s){Colors.RESET}")
                    else:
                        logging.warning(f"{Colors.RED}🚨 {name} | 0 publishers | Canal sem ingest!{Colors.RESET}")

                except Exception as e:
                    logging.error(f"{Colors.RED}❌ {name} | Erro: {e}{Colors.RESET}")

            logging.info(f"{Colors.BOLD}⏳ Aguardando {self.interval} segundos para próxima verificação...{Colors.RESET}\n")
            time.sleep(self.interval)


if __name__ == "__main__":
    try:
        monitor = ChannelHealthMonitor(interval_seconds=8)  # você pode mudar o intervalo aqui
        monitor.monitor()
    except KeyboardInterrupt:
        print("\n\n👋 Monitor encerrado pelo usuário.")
    except Exception as e:
        logging.error(f"{Colors.RED}Erro fatal: {e}{Colors.RESET}")