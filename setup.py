from setuptools import setup , find_packages
setup( 
    name='mcqgenerator', 
    version='0.0.1', 
    # description='A sample Python package', 
    author='Deepak Yadav', 
    author_email='honestharry1945@gmail.com', 
    packages=find_packages(), 
    install_requires=[ 
        'numpy', 
        'pandas', 
        'openai',
        'langchain',
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ], 
)