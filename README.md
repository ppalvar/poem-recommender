# Poetry recomender

This project is a RAG that recommends poems based on the user prompt.

The LLM used is Mistral AI (free version since this is only a school project and will be soon consigned to oblivion).

The dataset comes from [here](https://www.kaggle.com/datasets/michaelarman/poemsdataset).

You may install this libraries before running it:

```txt
pip install mistralai, numpy, sklearn
```

The `data.zip` contains example data (with all metadata already generated).

If you want to add your own data, just put a bunch of poems in `.txt` files inside the `data` directory on the project root. Then run `python preprocess.py` to process them all and generate metadata.

You also need a `.env` file with your [Mistral AI](https://mistral.ai/) api key like this:

```txt
MISTRAL_API_KEY=<your-key>
```
