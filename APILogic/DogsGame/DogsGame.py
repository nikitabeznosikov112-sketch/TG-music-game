import httpx
import random
import asyncio


DOGS =  [
    'affenpinscher', 'african', 'airedale', 'akita', 'appenzeller',
    'australian-kelpie', 'australian-shepherd', 'bakharwal', 'basenji',
    'beagle', 'bluetick', 'borzoi', 'bouvier', 'boxer', 'brabancon',
    'briard', 'buhund', 'bulldog-boston', 'bulldog-english', 'bulldog-french',
    'bullterrier', 'cattledog', 'cavapoo', 'chihuahua', 'chippiparai',
    'chow', 'clumber', 'cockapoo', 'collie-border', 'coonhound',
    'corgi', 'cotondetulear', 'dachshund', 'dalmatian', 'dane-great',
    'danishswedish', 'deerhound', 'dhole', 'dingo', 'doberman',
    'elkhound', 'entlebucher', 'eskimo', 'finnish', 'frise',
    'gaddi', 'german-shepherd', 'greyhound-indian', 'greyhound-italian',
    'groenendael', 'havanese', 'hound-afghan', 'hound-basset', 'hound-blood',
    'hound-english', 'hound-ibizan', 'hound-plott', 'hound-walker',
    'husky', 'keeshond', 'kelpie', 'kombai', 'komondor',
    'kuvasz', 'labradoodle', 'labrador', 'leonberg', 'lhasa',
    'malamute', 'malinois', 'maltese', 'mastiff-bull', 'mastiff-english',
    'mastiff-indian', 'mastiff-tibetan', 'mexicanhairless', 'mix',
    'mountain-bernese', 'mountain-swiss', 'mudhol', 'newfoundland',
    'otterhound', 'ovcharka', 'papillon', 'pariah', 'pekinese',
    'pembroke', 'pinscher', 'pitbull', 'pointer-german', 'pointer-germanlonghair',
    'pomeranian', 'poodle-medium', 'poodle-miniature', 'poodle-standard',
    'poodle-toy', 'pug', 'puggle', 'pyrenees', 'rajapalayam',
    'redbone', 'retriever-chesapeake', 'retriever-curly', 'retriever-flatcoated',
    'retriever-golden', 'ridgeback', 'rottweiler', 'rough-collie',
    'saluki', 'samoyed', 'schipperke', 'schnauzer-giant', 'schnauzer-miniature',
    'segugio', 'setter-english', 'setter-gordon', 'setter-irish',
    'sharpei', 'sheepdog-english', 'sheepdog-indian', 'sheepdog-shetland',
    'shiba', 'shihtzu', 'spaniel-blenheim', 'spaniel-brittany', 'spaniel-cocker',
    'spaniel-irish', 'spaniel-japanese', 'spaniel-sussex', 'spaniel-welsh',
    'spitz-indian', 'spitz-japanese', 'springer', 'stbernard',
    'terrier-american', 'terrier-andalusian', 'terrier-australian', 'terrier-bedlington',
    'terrier-border', 'terrier-boston', 'terrier-cairn', 'terrier-dandie',
    'terrier-fox', 'terrier-irish', 'terrier-kerryblue', 'terrier-lakeland',
    'terrier-norfolk', 'terrier-norwich', 'terrier-patterdale', 'terrier-russell',
    'terrier-scottish', 'terrier-sealyham', 'terrier-silky', 'terrier-tibetan',
    'terrier-toy', 'terrier-welsh', 'terrier-westhighland', 'terrier-wheaten',
    'terrier-yorkshire', 'terrvuren', 'vizsla', 'waterdog', 'weimaraner',
    'whippet', 'wolfhound'
]

async def get_dogs():
    gamedogs = random.sample(DOGS, 4)
    correct_answer = random.choice(gamedogs)

    api_dog = correct_answer.replace('-', '/')
    url = f'https://dog.ceo/api/breed/{api_dog}/images/random'

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)

            if response.status_code == 200:
                data = response.json()
                photo = data['message']

                return {'dogs': gamedogs, 'correct_answer': correct_answer, 'photo': photo}
            else:
                print('Ошибка в API')
                return ('Ошибка в API') 
        except Exception as e:
            print(e)
            return ('Ошибка')
        


