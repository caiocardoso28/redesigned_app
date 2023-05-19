
# SUBJECTS
portuguese_subject = 'Gartner | Seu call de introdução às ferramentas está disponível'
english_subject = 'Accept or Reschedule > Your Gartner Membership'
spanish_subject = 'Confirmar o proponer: Membresía de Gartner – Su sesión de capacitación'
french_subject = None

# BIs
portuguese_bi = """Notamos que você ainda não selecionou um outro horário para o seu tour do portal e do app. Portanto, proponho este para explorarmos os seus novos recursos dentro do Gartner.com. para otimizar o seu uso das funcionalidades.\n
Além de responder as suas perguntas, revisaremos:
•	Como procurar pesquisas relevantes eficientemente
•	Customizar o mural de notícias inteligente
•	Comunicar com outros clientes via o nosso fórum de discussões\n
Antes da reunião, afim de maximizar o nosso tempo, peço que:
•	Baixe o nosso app My Gartner Mobile (Versão IOS / Versão Android)
•	Realize o login no seu portal do Gartner –  Se estiver procurando procurando o seu usuário e senha, clique aqui para resetar a sua senha ou usuário: https://www.gartner.com/account/recover
•	Procure ter acesso ao seu notebook/computador para a sessão

Estou animado para falar contigo. Se você não estiver disponível neste horário por favor responder “RESCHEDULE” a este email e proporei um novo horário.
"""
english_bi = """I look forward to holding this time to review and tailor your Gartner.com Platform experience to align with your initiatives. If for any reason this date or time does not work with your calendar, please feel free to suggest an alternative. 
You’ll find the meeting information and a call agenda below.\n 
AGENDA: 
•       Showcasing content tailored to your priorities and initiatives 
•       Customizing your smart news feed and personal library\n 
BEFORE THE MEETING: 
•       Please download our Gartner Mobile App (App Store or Play Store) 
•       Please log in to your Gartner Platform – click here to recover login: https://www.gartner.com/account/recover
Please have access to your laptop/computer for the session.\n 
I am looking forward to speaking to you.
"""
spanish_bi = """Me gustaría proponer este momento para repasar sus nuevos recursos dentro de Gartner.com y resaltar los recursos digitales a su disposición para maximizar el valor de sus servicios de Gartner.

Entre las respuestas a sus preguntas iniciales, abordaremos:
•	Recuperar y mostrar contenido relevante
•	Personalizar su fuente de noticias inteligente y su biblioteca personal
•	Colaboración con sus pares a través de nuestra función de redes sociales

Antes de la reunión:
•	Instale la aplicación móvil de Gartner (IOS Versión / Android Versión)
•	Inicie sesión en su portal de Gartner – Para obtener sus credenciales de inicio de sesión, haga clic aquí: https://www.gartner.com/account/recover
•	Tenga acceso a su computadora para compartir su pantalla durante la sesión

Espero poder hablar usted, sin embargo, si no puede conectarse a la llamada, responda "REPROGRAMAR" a este correo electrónico y le propondré una nueva sesión.   

"""
french_bi = None

# AE
portuguese_ae = None
english_ae = None
spanish_ae = None
french_ae = None

# multi-AE
portuguese_multi_ae = None
english_multi_ae = None
spanish_multi_ae = None
french_multi_ae = None

# outreach
portuguese_outreach = None
english_outreach = None
spanish_outreach = None
french_outreach = None

countries = {'BRAZIL': {"Templates": {'BLIND_INVITE': portuguese_bi,
                                      'GREETING': "Oi",
                                      'AE_OUTREACH': portuguese_ae,
                                      'AE_GROUP_OUTREACH': portuguese_multi_ae,
                                      'OUTREACH': portuguese_outreach}, 'Language': 'Portuguese'},
             'CANADA': {"Templates": {'BLIND_INVITE': english_bi,
                                      'GREETING': "Hi",
                                      'AE_OUTREACH': english_ae,
                                      'AE_GROUP_OUTREACH': english_multi_ae,
                                      'OUTREACH': english_outreach}, 'Language': 'English'},
             'UNITED STATES': {"Templates": {'BLIND_INVITE': english_bi,
                                             'GREETING': "Hi",
                                             'AE_OUTREACH': english_ae,
                                             'AE_GROUP_OUTREACH': english_multi_ae,
                                             'OUTREACH': english_outreach}, 'Language': 'English'},
             'MEXICO': {"Templates": {'BLIND_INVITE': spanish_bi,
                                      'GREETING': "Hola",
                                      'AE_OUTREACH': spanish_ae,
                                      'AE_GROUP_OUTREACH': spanish_multi_ae,
                                      'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'COLUMBIA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                        'GREETING': "Hola",
                                        'AE_OUTREACH': spanish_ae,
                                        'AE_GROUP_OUTREACH': spanish_multi_ae,
                                        'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'SPAIN': {"Templates": {'BLIND_INVITE': spanish_bi,
                                     'GREETING': "Hola",
                                     'AE_OUTREACH': spanish_ae,
                                     'AE_GROUP_OUTREACH': spanish_multi_ae,
                                     'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'ARGENTINA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                         'GREETING': "Hola",
                                         'AE_OUTREACH': spanish_ae,
                                         'AE_GROUP_OUTREACH': spanish_multi_ae,
                                         'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'PERÚ': {"Templates": {'BLIND_INVITE': spanish_bi,
                                    'GREETING': "Hola",
                                    'AE_OUTREACH': spanish_ae,
                                    'AE_GROUP_OUTREACH': spanish_multi_ae,
                                    'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'VENEZUELA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                         'GREETING': "Hola",
                                         'AE_OUTREACH': spanish_ae,
                                         'AE_GROUP_OUTREACH': spanish_multi_ae,
                                         'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'CHILE': {"Templates": {'BLIND_INVITE': spanish_bi,
                                     'GREETING': "Hola",
                                     'AE_OUTREACH': spanish_ae,
                                     'AE_GROUP_OUTREACH': spanish_multi_ae,
                                     'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'ECUADOR': {"Templates": {'BLIND_INVITE': spanish_bi,
                                       'GREETING': "Hola",
                                       'AE_OUTREACH': spanish_ae,
                                       'AE_GROUP_OUTREACH': spanish_multi_ae,
                                       'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'GUATEMALA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                         'GREETING': "Hola",
                                         'AE_OUTREACH': spanish_ae,
                                         'AE_GROUP_OUTREACH': spanish_multi_ae,
                                         'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'CUBA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                    'GREETING': "Hola",
                                    'AE_OUTREACH': spanish_ae,
                                    'AE_GROUP_OUTREACH': spanish_multi_ae,
                                    'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'BOLIVIA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                       'GREETING': "Hola",
                                       'AE_OUTREACH': spanish_ae,
                                       'AE_GROUP_OUTREACH': spanish_multi_ae,
                                       'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'DOMINICAN REPUBLIC': {"Templates": {'BLIND_INVITE': spanish_bi,
                                                  'GREETING': "Hola",
                                                  'AE_OUTREACH': spanish_ae,
                                                  'AE_GROUP_OUTREACH': spanish_multi_ae,
                                                  'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'HONDURAS': {"Templates": {'BLIND_INVITE': spanish_bi,
                                        'GREETING': "Hola",
                                        'AE_OUTREACH': spanish_ae,
                                        'AE_GROUP_OUTREACH': spanish_multi_ae,
                                        'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'PARAGUAY': {"Templates": {'BLIND_INVITE': spanish_bi,
                                        'GREETING': "Hola",
                                        'AE_OUTREACH': spanish_ae,
                                        'AE_GROUP_OUTREACH': spanish_multi_ae,
                                        'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'EL SALVADOR': {"Templates": {'BLIND_INVITE': spanish_bi,
                                           'GREETING': "Hola",
                                           'AE_OUTREACH': spanish_ae,
                                           'AE_GROUP_OUTREACH': spanish_multi_ae,
                                           'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'NICARAGUA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                         'GREETING': "Hola",
                                         'AE_OUTREACH': spanish_ae,
                                         'AE_GROUP_OUTREACH': spanish_multi_ae,
                                         'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'COSTA RICA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                          'GREETING': "Hola",
                                          'AE_OUTREACH': spanish_ae,
                                          'AE_GROUP_OUTREACH': spanish_multi_ae,
                                          'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'PANAMA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                      'GREETING': "Hola",
                                      'AE_OUTREACH': spanish_ae,
                                      'AE_GROUP_OUTREACH': spanish_multi_ae,
                                      'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'URUGUAY': {"Templates": {'BLIND_INVITE': spanish_bi,
                                       'GREETING': "Hola",
                                       'AE_OUTREACH': spanish_ae,
                                       'AE_GROUP_OUTREACH': spanish_multi_ae,
                                       'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'PUERTO RICO': {"Templates": {'BLIND_INVITE': spanish_bi,
                                      'GREETING': "Hola",
                                      'AE_OUTREACH': spanish_ae,
                                      'AE_GROUP_OUTREACH': spanish_multi_ae,
                                      'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             'EQUATORIAL GUINEA': {"Templates": {'BLIND_INVITE': spanish_bi,
                                                 'GREETING': "Hola",
                                                 'AE_OUTREACH': spanish_ae,
                                                 'AE_GROUP_OUTREACH': spanish_multi_ae,
                                                 'OUTREACH': spanish_outreach}, 'Language': 'Spanish'},
             }

