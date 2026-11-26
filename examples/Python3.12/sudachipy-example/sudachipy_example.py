from sudachipy import dictionary, tokenizer


def demonstrate_sudachipy():
    """
    Demonstrates user-facing Japanese NLP capabilities of SudachiPy.
    Each section can be read and run independently.
    """
    tokenizer_obj = dictionary.Dictionary().tokenizer()
    text = "国家公務員試験を受けるために、東京へ行きました。"

    print("=== 1. Tokenization with Split Modes (A / B / C) ===")
    print(f"Text: {text}")
    modes = {
        "A (short unit)": tokenizer.Tokenizer.SplitMode.A,
        "B (middle unit)": tokenizer.Tokenizer.SplitMode.B,
        "C (named entity / long unit)": tokenizer.Tokenizer.SplitMode.C,
    }
    for name, mode in modes.items():
        surfaces = [m.surface() for m in tokenizer_obj.tokenize(text, mode)]
        print(f"  Mode {name}: {surfaces}")
    print()

    print("=== 2. Morpheme Details (Mode C) ===")
    mode_c = tokenizer.Tokenizer.SplitMode.C
    for m in tokenizer_obj.tokenize(text, mode_c):
        print(
            f"  {m.surface():<8} reading={m.reading_form():<10} "
            f"dict_form={m.dictionary_form():<8} pos={m.part_of_speech()[0]}"
        )
    print()

    print("=== 3. Text Normalization ===")
    variants = ["打込む", "打ち込む", "うちこむ", "附属", "付属", "ｱｲｳｴｵ"]
    for word in variants:
        normalized = [m.normalized_form() for m in tokenizer_obj.tokenize(word, mode_c)]
        print(f"  {word} -> {''.join(normalized)}")
    print()

    print("=== 4. Dictionary (Lemma) Form of Inflected Verbs ===")
    for sentence in ["食べました", "走っている", "見たくなかった"]:
        lemmas = [m.dictionary_form() for m in tokenizer_obj.tokenize(sentence, mode_c)]
        print(f"  {sentence} -> {lemmas}")
    print()

    print("=== 5. Part-of-Speech Filtering (extract nouns) ===")
    article = "今日は天気が良いので、公園で友達と野球をしました。"
    nouns = [
        m.surface()
        for m in tokenizer_obj.tokenize(article, mode_c)
        if m.part_of_speech()[0] == "名詞"
    ]
    print(f"  Text: {article}")
    print(f"  Nouns: {nouns}")
    print()

    print("=== 6. Out-of-Vocabulary (OOV) Detection ===")
    for m in tokenizer_obj.tokenize("ゔゔゔ", mode_c):
        print(f"  {m.surface()}: is_oov={m.is_oov()}")
    print()

    print("=== Script Complete ===")


if __name__ == "__main__":
    demonstrate_sudachipy()
