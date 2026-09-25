from setuptools import setup,find_packages
from typing import List

HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    requirement=[]
    with open(file_path) as f:
        requirement=f.readlines()
        requirement=[req.replace('\n','') for req in requirement]
    if HYPHEN_E_DOT in requirement:
        requirement.remove(HYPHEN_E_DOT)
    return requirement
setup (
    name="social_media_impact",
    version='0.1',
    description="ML model to predict the social media impact",
    author="Spandan Sarkar",
    author_email='spandansarkarofficial06@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)