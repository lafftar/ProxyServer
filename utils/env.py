import asyncio
import sys
import encodings.idna
from faker import Faker

from all_utils.custom_logger import logger
from all_utils.root import get_project_root

FAKE = Faker()

CA_TIMEZONES = [
    'America/Halifax',
    'America/Winnipeg',
    'America/Toronto',
    'America/Edmonton',
    'America/St_Johns',
    'America/Vancouver',
    'America/Regina',
    'America/Whitehorse'
]

CITIES = [
    'Calgary',
    'Vancouver',
    'Winnipeg',
    'Moncton',
    "St. John's",
    'Yellowknife',
    'Halifax',
    'Iqaluit',
    'Toronto',
    'Charlottetown',
    'Montreal',
    'Saskatoon',
    'Whitehorse',
]

DEBUG_RUN = False  # some fx's mess with the pycharm console, turn this to false for those.
with open(f'{get_project_root()}/proxies/isps.txt') as file:
    ISPS = [f'http://{line.strip()}' for line in file.readlines()]

with open(f'{get_project_root()}/proxies/geo.txt') as file:
    RESIS = [f'{line.strip()}' for line in file.readlines()]


with open(f'{get_project_root()}/config.txt') as file:
    settings = {
        line.strip().split(' -> ')[0]: line.strip().split(' -> ')[1]
        for line in file.readlines()
    }
    CATCHALLS = [email for email in settings['CATCHALLS'].split(' | ')]
    # two names, only
    NAMES = [names.split() for names in settings['NAMES'].split(' | ')]
    # should be at least 8 characters
    PASSWORD = settings['PASSWORD']
    # just 4 character year of birth
    BIRTHYEAR = settings['BIRTHYEAR']
    GMAILS = [gmail.strip().split(',') for gmail in settings['GMAILS'].split(' | ')]
    FAIL_RATE = int(settings['FAIL_RATE'])

if sys.platform == 'win32':
    import win32file
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    win32file._setmaxstdio(8192)

if sys.platform == 'linux':
        import resource
        before, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        try:
            resource.setrlimit(resource.RLIMIT_NOFILE, (1048576, hard))
            after, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            logger().info(f'\n'
                          f'\tRaised max limit\n'
                          f'\tPrevious Limit - {before}\n'
                          f'\tNew Limit - {after}')
        except ValueError:
            logger().warning(f'Already at max limit - {before}')


ASCII_ART = """                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                           @@@@                             @@@@                
                                                            @@@    @@@          
         @@@   @@@#   @@@  @@@   @@@@@@@@@    @@@@   @@@@   @@@    @@@          
         @@@   @@@#   @@@  @@@   @@@@   @@@@    @@@@@@@    @@@@    @@@          
         @@@   @@@#   @@@  @@@   @@@     @@@     *@@@#     @@@@@@@@@@@@@        
         @@@   @@@@  &@@@  @@@   @@@     @@@    @@@,@@@    @@@@@@@@@@@@@        
          @@@@@@@@@@@@@(   @@@   @@@     @@@  @@@@   @@@@          @@@          
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                """