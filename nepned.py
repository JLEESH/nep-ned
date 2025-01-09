from pydantic import BaseModel
from openai import OpenAI

class HybridLanguageTranslation(BaseModel):
    original: str
    hybrid: str
    translation: str

oa_key = None  # replace with caution
DUMMY_RESPONSE_PATH = "sample_responses/dummy_response"
DEFAULT_RESP_PATH = "./output/responses/"
DEFAULT_TRANSLATION_PATH = "./output/tl_json/"
DEFAULT_TEXT_PATH = "./output/translations/"

TRANSLATOR_SYSTEM_PROMPT = """
    You are a tool to translate English text into Dutchm but modified to be more like English.
    Translate English text into an alternate version of Dutch that is more accessible to English speakers.
    The goal is to create a recognizable hybrid, where English speakers can infer the meaning, but the text appears distinctly Dutch.
    For example:

        English: "The house by the water is small."
        Dutch: "Het huis bij het water is klein."
        Hybrid: "De huus bij de water is smal."
    
    Try to preserve Dutch words where the meaning can be at all inferred by English speakers:
    
        English "Dutch" -> Dutch "nederlands" instead of "dutsch".
        English "water" -> Dutch "water" instead of a overly-malformed "watur".
        English "German" -> Dutch "duits" instead of a malformed version "jerman".

    Most importantly, these substitutions shoud be consistent with Dutch-style spelling conventions,
    while prioritizing clarity for English speakers.
    
    The alternate form of the language should:
    - Be recognizable as Dutch to English speakers.
    - Use Dutch-like spellings for vocabulary to create a recognizable hybrid language.
    - Make the text accessible to English speakers while appearing distinctly Dutch.
    - Preserve the meaning of the original text.

    Return response in the form of a JSON object with the following keys:

    Response JSON format:

    {
        "original": "The house by the water is small.",
        "hybird": "De huus bij de water is smal.",
        "translation": "Het huis bij het water is klein."
    }

    More examples: 
    {
        "original": "We have a serious problem. We are not using nearly enough nep Dutch.",
        "hybrid": "We hebbe een serieus probleem. We üsen niet naarlig genoeg nep nederlands.",
        "translation": "We hebben een serieus probleem. We gebruiken niet bijna genoeg nep Nederlands."
    }

    {
        "original": "This is a sample sentence of nep Dutch. It is very fun to do something like this.",
        "hybrid": "Dis is een sample zentence van nep Nederlants. Het is erg fun som ding lijk dis te doen.",
        "translation": "Dit is een voorbeeldzin van nep Nederlands. Het is erg leuk om zoiets te doen."
    }

    {
        "original": "Soon, nep Dutch will rule the world. Truly the world will know of the one true language.",
        "hybrid": "Soen zal nep Nederlands de wereld rulen. Truly zal de wereld kennen van de een trouwe taal.",
        "translation": "Binnenkort zal nep Nederlands de wereld regeren. Truly zal de wereld weten van de één echte taal."
    }

    If the user asks for a sample sentence instead, generate a new sentence on your own and perform the rest of the task.
"""
# e.g. python3.12 nepned.py -t "(Instead of translating a given sentence give a sample sentence instead)"

TRANSLATOR_USER_PROMPT = "Translate the following text into the alternate Dutch-like English form:\n{input_text}"

def generate_translation(input_text, oa_key=oa_key, dummy=False):
    """
        Translate the input text into a Dutch-like English form.

        Returns the translated text and the response object.
    """
    if dummy:
        return generate_response(TRANSLATOR_SYSTEM_PROMPT, TRANSLATOR_USER_PROMPT.format(input_text=input_text), oa_key=oa_key, dummy=True)
    
    response = generate_response(TRANSLATOR_SYSTEM_PROMPT, TRANSLATOR_USER_PROMPT.format(input_text=input_text), oa_key=oa_key)
    hybridLangTL = response.choices[0].message.parsed

    hybridLangTL_full_json_dict = hybridLangTL.model_dump(mode="json")
    hybridLangTL_full_json_text = hybridLangTL.model_dump_json(indent=4)
    
    hybrid_text = hybridLangTL_full_json_dict["hybrid"]
    
    translation_obj = {
        "original" : hybridLangTL_full_json_dict["original"],
        "hybrid" : hybrid_text,
        "translation" : hybridLangTL_full_json_dict["translation"],
        "json_dict" : hybridLangTL_full_json_dict,
        "json_text" : hybridLangTL_full_json_text,
        "response" : response
    }

    return translation_obj
    


def generate_response(system_text, user_text, oa_key=oa_key, dummy=False):
    if dummy:
        return load_response_var(DUMMY_RESPONSE_PATH)
    if oa_key is None:
        raise ValueError("OpenAI API key is not set.")

    client = OpenAI(api_key=oa_key)

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text},
        ],
        response_format=HybridLanguageTranslation,
    )

    #hybridLangTL = response.choices.messages[0].parsed

    # old version
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": system_text},
    #         {"role": "user", "content": user_text},
    #     ],
    #     response_format={"type": "text"},
    #     temperature=1,
    #     max_completion_tokens=2048,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    # )

    return response


def save_translation(translation, id=None, filename=None):
    """
        Save translation.json to file.
    """
    if filename is None:
        if id is None:
            import uuid
            filename = f"translation_{uuid.uuid4()}.json"
        else:
            filename = f"translation_{id}.json"
    
    with open(filename, "w") as f:
        f.write(translation)

def save_text(text, id=None, filename=None):
    """
        Save text output to file.
    """
    if filename is None:
        if id is None:
            import uuid
            filename = f"neperlands_{uuid.uuid4()}.json"
        else:
            filename = f"neperlands_{id}.json"
    
    with open(filename, "w") as f:
        f.write(text)


def save_response_content_text(response, id=None, filename=None):
    if filename == None:
        if id == None:
            import uuid
            filename = f"response_content_text_{uuid.uuid4()}.txt"
        else:
            filename = f"response_content_text_{id}.txt"
    
    with open(filename, "w") as f:
        f.write(response.choices[0].message.content)


def save_response_text(response, id=None, filename=None):
    if filename == None:
        if id == None:
            import uuid
            filename = f"response_text_{uuid.uuid4()}.txt"
        else:
            filename = f"response_text_{id}.txt"
    
    with open(filename, "w") as f:
        f.write(repr(response))


def save_response_var(response, id=None, filename=None):
    import pickle

    if filename is None:
        if id is None:
            filename = "response.txt"
        else:
            filename = f"response_{id}.txt"

    with open(filename, "wb") as f:
        pickle.dump(response, f)


def load_response_var(filename):
    if filename is None:
        raise ValueError("load_response_var: filename is None.")

    import pickle
    try:
        with open(filename, "rb") as f:
            loaded_response = pickle.load(f)
        return loaded_response
    except FileNotFoundError as e:
        print(f"WARNING: load_response_var: File not found: {filename}")
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text", "-t", required=True, help="Input text to translate.")
    #DEFAULT_TL_TEXT = "This is a sample sentence of nep Dutch. It is very fun to do something like this!"
    #parser.add_argument("--text", "-t", type=str, default=DEFAULT_TL_TEXT, help="Input text to translate.")
    parser.add_argument("--dummy", "-D", action="store_true", default=False, help="Run in dummy mode.")
    #parser.add_argument("--save", "-s", action="store_true", default=False, help="Save the translation response.")
    parser.add_argument("--verbosity", "-v", type=int, default=5, help="Level of verbosity.")

    parser.add_argument("--path-translation-text", "-p", type=str, default=DEFAULT_TEXT_PATH, help="Set path to save the text outputs.")
    parser.add_argument("--path-translation-json", "-j", type=str, default=DEFAULT_TRANSLATION_PATH, help="Set path to save the translation JSON files.")
    parser.add_argument("--path-response", "-r", type=str, default=DEFAULT_RESP_PATH, help="Set path to save the responses.")
    parser.add_argument("--generate-response", "-g", dest="GEN_RES_SAVE", action="store_true", default=False, help="Save API response to file.")
    args = parser.parse_args()

    DUMMY = args.dummy
    #SAVE = args.save
    M_GEN_RES_SAVE = args.GEN_RES_SAVE
    TRANSLATION_PATH = args.path_translation_json.strip()
    TEXT_PATH = args.path_translation_text.strip()
    RESP_PATH = args.path_response.strip()
    input_text = args.text.strip()
    verbosity = args.verbosity

    import os
    if os.path.exists(TRANSLATION_PATH) == False:
        os.makedirs(TRANSLATION_PATH)

    # load .env file to obtain OpenAI API key
    from dotenv import load_dotenv

    load_dotenv()
    oa_key = os.getenv("OPENAI_API_KEY")
    if oa_key is None:
        raise ValueError("Main: OpenAI API key is not set.")

    # obtain response
    if verbosity > 2:
        print("Requesting translation...")
    translation_obj = generate_translation(input_text, oa_key, dummy=DUMMY)
    if verbosity > 2:
        print("Translation obtained.")
    print()

    # process output
    response = translation_obj["response"]
    translation_json = translation_obj["json_text"]
    hybrid_text = translation_obj["hybrid"]

    # print some results to terminal
    formatted_output_text = ""
    if verbosity > 3:
        print(f"English: {translation_obj["original"]}\n")
        formatted_output_text = ''.join([formatted_output_text, f"English: {translation_obj["original"]}\n"])
    
    print(f"Neperlands: {hybrid_text}\n")
    formatted_output_text = ''.join([formatted_output_text, f"Neperlands: {hybrid_text}\n"])
    
    if verbosity > 4:
        print(f"Dutch: {translation_obj["translation"]}\n")
        formatted_output_text = ''.join([formatted_output_text, f"Dutch: {translation_obj["translation"]}\n"])
    
    print(formatted_output_text)

    # save response to file
    import uuid
    file_uuid = str(uuid.uuid4())
    if DUMMY:
        file_uuid = "dummy_" + file_uuid
    filename_translation = TRANSLATION_PATH + f"translation_{file_uuid}.json"
    filename_fot = TEXT_PATH + f"neperlands_{file_uuid}.txt"

    #filename_var = RESP_PATH + f"response_{file_uuid}.txt"
    filename_text = RESP_PATH + f"response_text_{file_uuid}.txt"
    filename_content_text = RESP_PATH + f"response_content_text_{file_uuid}.txt"

    if M_GEN_RES_SAVE:
        #save_response_var(response, id=file_uuid, filename=filename_var)
        save_response_text(response, id=file_uuid, filename=filename_text)
        save_response_content_text(response, id=file_uuid, filename=filename_content_text)
    
    save_translation(translation_json, id=file_uuid, filename=filename_translation)
    save_text(formatted_output_text, id=file_uuid, filename=filename_fot)

    return response


if __name__ == "__main__":
    main()
