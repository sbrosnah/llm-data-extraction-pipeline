# LLM Data Extraction Pipeline

This is a modular and flexible framework for LLM-powered data extaction from text. This project makes it easy to create and combine stages. This is by no means an 'out of the box' solution as that would surrender a lot of the flexibility. Instead, the groundwork is laid for you to quickly create and iterate on LLM-powered stages of your extraction pipeline.

The flexibility of this framework comes from the fact that the core features have been extracted out and the extraction module depends on a strategy object (lookup the strategy pattern or see the entity extraction example in the code if you are unfamiliar with the how the strategy pattern works. You should understand it to be able to use this project effectively). It is your job to implement the functions in the strategy object for each stage of the pipeline. 

## Features

- **Logging**: LLM and User Message Logging
- **Retry logic**: Retry logic for invalid outputs from the LLM
- **Output parsing**: Can parse out LLM thinking and JSON outputs.
- **Chunk iteration and gleaning**: Iterative data extraction of chunks where the number of gleanings on each chunk is configurable.
- **Reusability**: The design patterns implemented in this project make the code extremely reusable. 

## Installation

Just ensure your system has the OpenAI library installed for the example code. However, this project doesn't require you to install the OpenAI library. You just need to install whichever model projeder library you are using 
for the LLM set in the extraction configs of the pipeline stages. This will make more sense later. 

## Quick Start

See main.py for an example of how to use this project. There, you will see an example of how to implement a stage of a pipeline that is intended for entity extraction. 

There, you will find a model.py file that contains models used specifically for the strategy in this stage. You will also find a strategy_functions.py file that contains the functions used in teh construction of the 'ExtractionStrategy' implementation. These are kept in a separate file so that you can try different functions without losing your work. These functions can then be imported into the model.py file where the Strategy object is created. 

In the prompts.py file, you will find prompts that are used in the strategy_functions.py file to construct user messages. In the entity extraction prompts you will see that there is a list of guidelines with examples so that I can dynamically choose which guidelines I would like to use in the prompt without having to explicitly change the prompt. 

The examples directory contains the examples in a structured format. 


## Configuration

Set up the logging configuration in the config/logging.yaml file for each stage of your extraction pipeline. There you will see an example of the configuration for the entity extraction log used in the example. 

For each stage in your pipeline, you will want to create a directory with the subdirectories 'logs', 'prompts', 'examples', and 'results'. You can then 

## Project Status

This project is mainly for personal use to make development of a data extraction pipeline I'm working on a lot easier. There is still a lot of work I am planning on doing in this project.

I plan to:
- Improve documentation
- Implement a reusable testing framework that users can customize (specific to data extraction) using a dataset and LLM as a judge. 
- Integrate with a database so not everything is getting stored in json files.

