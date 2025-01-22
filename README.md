# Consilium
![Consilium Logo](https://github.com/user-attachments/assets/a421f1d8-4e09-4350-bf8a-0ca70b59b462)

## What is it?
__Consiluim__ is a generative model designed to provide accurate and concise answers to questions about the Uruguayan Constitution. Trained on a dataset of constitutional articles and legal content built also in the scope of this project, the model generates responses based on real-world queries. Its primary aim is to enhance accessibility to legal information, offering users an intuitive way to retrieve relevant insights into constitutional law.

## Motivation
The motivation behind _Consiluim_ is to improve access to legal information, specifically concerning the Uruguayan Constitution. By leveraging machine learning techniques, the project aims to bridge the gap between complex legal texts and everyday users, allowing for quick and understandable answers to constitutional questions. This project responds to the need for an efficient, user-friendly tool that can facilitate better understanding of the law, whether for students, professionals, or anyone interested in the legal framework of Uruguay. Through _Consiluim_, users can engage with the Constitution in a more dynamic and approachable way.

## Characteristics
- [x] English based.
- [x] Trained on the Uruguayan Constitution.
- [x] Generates answers to constitutional inquiries.
- [x] Training dataset includes real-world questions on some articles.

## Instalation
Before being able to try this project out there are some requirements that need to be met:


## Usage


## Model Evaluation


## Data

### Quick note about the lack of validation and test dataset
Currently, the project does not have a separate validation or test dataset. The focus has been on training the model with a small dataset, which consists of questions related to the articles of the Uruguayan Constitution. Using examples from the same dataset for validation would limit the model's ability to learn useful information, as it would be exposed to the same data during both training and evaluation phases.

This decision is also due to the tight project timeline. The project has a 5-week duration, and during the first week, the primary focus was on collecting the necessary data. In the second week, I encountered several challenges with model selection and training, and it took time to settle on GPT-2. Once the model was chosen, I had to create the dataset from scratch, which added significant time. The training process itself took 8 days to complete with the dataset available.

Given the time constraints and the need to ensure the project could be concluded within the deadlines, I prioritized model training over creating a separate validation set. Adding more data for validation at this stage would have risked delaying the project and potentially compromising the completion of the defense.

### Data extraction
The data used for the training of this model was extracted from two main sites:
- [Parlamento](https://parlamento.gub.uy/)
- [IMPO](https://www.impo.com.uy/)

Using the ``model/data_extraction/main_extract_data.py``

### Data preprocessing

## Results


## Future Improvements  
This project is still under development, with the following features under consideration:  

- [ ] **Multilingual Support** ..... Add support for Spanish and Russian to make the model accessible to a broader audience.
- [ ] **Expanded Dataset** ......... Finish the current dataset and add new legal texts to improve the model's coverage and utility.
- [ ] **Optimized Data Loading** ... Enhance the efficiency of training data handling for faster performance.  
- [ ] **User-Friendly Web Page** ... Create an interactive web interface to simplify interaction with the model.  
- [ ] **Hyperparameter tunning** ... Refine model performance through systematic hyperparameter tuning and rigorous evaluation metrics to ensure robustness.
- [ ] **Automated Dataset** ........ Further streamline the process of generating and variating datasets to save time and reduce manual effort.
- [ ] **Validation Dataset** ....... Create a separate validation and test dataset to assess model performance without overlapping with the training data, ensuring the model generalizes well to unseen data.


## Contact Information
If you have any questions, suggestions, or comments, feel free to reach out through any of the following channels:

- __Email__ ........ emanueltrias9@gmail.com
- __LinkedIn__ ..... [Emanuel Trias](https://www.linkedin.com/in/emanuel-trias-86641a280/)
- __GitHub__ ....... [KrasniKot](https://github.com/KrasniKot)
