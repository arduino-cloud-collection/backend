from setuptools import setup

setup(
    name='arduino_backend',
    version='0.1',
    packages=['arduino_backend', 'arduino_backend.user', 'arduino_backend.auth'],
    url='https://github.com/arduino-cloud-collection/backend',
    license='GPL',
    author='Yannis Storrer',
    author_email='yannis.storrer@web.de',
    description='The backend for the arduino-cloud project',
    install_requires=[
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'psycopg2-binary',
        'python-jose',
        'python-multipart',
        'blake3',
        'bcrypt'
    ]
)
