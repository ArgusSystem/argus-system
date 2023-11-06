import os

DIR = 'datasets/scene_of_the_crime/people'

walker = os.walk(DIR)

_, people, _ = next(walker)

for person in people:
    directory, _, photos = next(walker)

    def sorting_key(p):
        if '_' in p:
            return int(p.split('_')[1].split('.')[0])

        return p

    for i, photo in enumerate(sorted(photos, key=sorting_key)):
        ending = photo.split('.')[1]
        src = f'{directory}/{photo}'
        dst = f'{directory}/{person}_{i + 1}.{ending}'

        if src != dst:
            os.rename(src, dst)
            print(f'{src} -> {dst}')

