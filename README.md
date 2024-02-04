# Cosmic Database Analysis GUI

A Method For Data parsing of COSMIC database files for Aging Related research.

## Description


This program provides a comprehensive tool for analyzing and visualizing data from the COSMIC Database. It efficiently parses downloaded data to generate insights on various metrics such as histology, age versus frequency, primary site and age correlations, amino acid mutation types, and the frequency of coding and noncoding mutations. It facilitates data visualization through integration with the cBioPortal Mutation Mapper and supports analysis with CRAVAT for VEST, CHASM+, and FATHMM scores.

The user interface includes a script that processes Cravat output to create inputs for the cBioPortal Mutation Mapper. This includes identifying significant missense mutations and generating files necessary for FOLDX molecular modeling. Additionally, the program offers a script for conducting Chi-Square Analysis on functional versus nonfunctional domains of genes, focusing on disruptive and nondisruptive regions.

Moreover, it features a script for modeling significant mutations, as determined by CRAVAT, on protein structures (PDB files). It calculates ΔΔG values for missense mutations and generates updated structural PDBs, providing a holistic view of the mutation impacts on protein function and structure. This suite of tools is designed to enhance the understanding of genetic mutations and their implications, streamlining the process from data parsing to advanced molecular modeling.

## Getting Started

### Dependencies

* Libraries that are required to run the program can be installed using this command:
```
pip3 install -r requirements.txt
```
* COSMICPARSE is able to operate on any machine with Python 3.8 or above.

### Installing(mac)
* navigate to the directory of the downloaded files and excute this command:
```
pyinstaller MainScrip.py
```
* In the dist folder there will be a Folder named MainScrip you can move this folder to wherever on your desktop is easily qaccessible. Within the MainScrip folder is an excutable that when double clicked will run the program. 

## Authors

Contributors names and contact info

* Shayne Skrtic (skrtics@xavier.edu)
* Designed Primarrily for Use in the Escorcia Lab https://www.xavier.edu/biology-department/escorcia-laboratory/index
