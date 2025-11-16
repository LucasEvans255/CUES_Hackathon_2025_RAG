# PROJECT TITLE: RAGebait — Detecting LLM Behavior Under Conflicting Evidence
## 🎯 Core Goal

Build a RAG-based evaluation system that intentionally retrieves contradictory documents and analyzes how LLM outputs behave under conflict:

Do they merge inconsistent facts?
Do they pick a side?
Do they resolve the conflict transparently?
Do they hallucinate explanations?
Do they hide contradictions?



## 🧩 Concept Overview

Source data from Wikipedia pages in different categories of content
Change key figures/facts in the chosen text that affect the central context/message
Upload modified information in a text file as context for Claude LLM
Prompt it with a query about information in the file
Evaluate the responses. 
Analyse how often the LLM hallucinates and in what area of knowledge does it hallucinate the most.

## Project Structure:
wiki-modifer: sources wikipedia pages and returns modified text
Phase2-CLI_chat: interfaces with Claude LLM. Allows upload of context documents (i.e. modified wikipedia texts in this case) and allows user to interact and prompt it. It's responses and behaviours are then analysed.


