# Roh-oh-mah-jee
# ©Peter Yanase, contact: yanase@kneedeepjapan.com
# Distributed under GPLv3.
# Roh-oh-mah-jee aims to automate the conversion between katakana and
# the phonetic notation proposed by Noda and Nakakita in the following paper:
# DOI: 10.15084/00001600

import re

youon = {
    "キャー": "kyahh", "キュー": "keww", "キョー": "kyohh",
    "シャー": "shahh", "シュー": "sheww", "ショー": "showw",
    "チャー": "chahh", "チュー": "cheww", "チョー": "chohh",
    "ニャー": "nyahh", "ニュー": "new", "ニョー": "nyohh",
    "ヒャー": "hyahh", "ヒュー": "heww", "ヒョー": "hyohh",
    "ミャー": "myahh", "ミュー": "meww", "ミョー": "myohh",
    "リャー": "ryahh", "リュー": "ryeww", "リョー": "ryoh",

    "ギャー": "gyahh", "ギュー": "gyooo", "ギョー": "gyohh",
    "ジャー": "jahh", "ジュー": "jeww", "ジョー": "jooe",
    "ビャー": "byaah", "ビュー": "beww", "ビョー": "byohh",
    "ピャー": "pyahh", "ピュー": "peww", "ピョー": "pyohh",

    "キャ": "kya", "キュ": "kyu", "キョ": "kyo",
    "シャ": "sha", "シュ": "shu", "ショ": "sho",
    "チャ": "cha", "チュ": "chew", "チョ": "cho",
    "ニャ": "nya", "ニュ": "nyu", "ニョ": "nyo",
    "ヒャ": "hya", "ヒュ": "hew", "ヒョ": "hyo",
    "ミャ": "mya", "ミュ": "mew", "ミョ": "myo",
    "リャ": "rya", "リュ": "ryu", "リョ": "ryo",

    "ギャ": "gya", "ギュ": "gyu", "ギョ": "gyo",
    "ジャ": "jah", "ジュ": "jew", "ジョ": "joh",
    "ビャ": "bya", "ビュ": "byu", "ビョ": "byo",
    "ピャ": "pya", "ピュ": "pew", "ピョ": "pyo",
    }

chokuon = {
    "ア": {
        "ア": "ah", "カ": "kah", "サ": "sah", "タ": "tah",
        "ナ": "nah", "ハ": "hah", "マ": "mah", "ヤ": "yah",
        "ラ": "rah", "ワ": "wa",

        "ガ": "gah", "ザ": "zah", "ダ": "dah",

        "バ": "bah", "パ": "pah",

        "ツァ": "tsa", "ファ": "fa",

        "ヴァ": "va",
        },
    "イ": {
        "イ": "ee", "キ": "kee", "シ": "she", "チ": "chee",
        "ニ": "nee", "ヒ": "hee", "ミ": "mee", "リ": "ree",

        "ギ": "ghee", "ジ": "jee",

        "ビ": "bee", "ピ": "pee",

        "ウィ": "wih", "ティ": "tea", "フィ": "fih",

        "ヴィ": "vih", "ディ": "dih",
        },
    "ウ": {
        "ウ": "woo", "ク": "koo", "ス": "su", "ツ": "tsu",
        "ヌ": "noo", "フ": "foo", "ム": "moo", "ユ": "you", "ル": "roo",

        "グ": "goo", "ズ": "zoo",

        "ブ": "boo", "プ": "poo",

        "トゥ": "to",

        "ヴ": "vu", "デュ": "dew", "ドゥ": "do",
        },
    "エ": {
        "エ": "eh", "ケ": "keh", "セ": "seh", "テ": "teh",
        "ネ": "neh", "ヘ": "heh", "メ": "meh", "レ": "reh",

        "ゲ": "geh", "ゼ": "zeh", "デ": "deh",

        "ベ": "beh", "ペ": "peh",

        "ウェ": "weh", "シェ": "sheh", "チェ": "che", "ツェ": "tseh", "フェ": "feh",

        "ヴェ": "veh", "ジェ": "jeh",
        },
    "オ": {
        "オ": "oh", "コ": "koh", "ソ": "soh", "ト": "toh",
        "ノ": "noh", "ホ": "hoe", "モ": "moh", "ヨ": "yoh", "ロ": "roh",

        "ゴ": "goh", "ゾ": "zoh", "ド": "doh",

        "ボ": "boh", "ポ": "poh",

        "ウォ": "wo", "ツォ": "tso", "フォ": "fo",

        "ヴォ": "vo",
        },
    "ン": {
        "ン": "n",
        }
    }


def convert_mora(mora: str, pronunciation: str, romanized: str) -> str:
    if mora in romanized:
        romanized = romanized.replace(mora, f"{pronunciation}-")
    return romanized


def romanize(katakana_string: str) -> str:
    romanized = katakana_string

    # 拗音の変換
    for mora, pronunciation in youon.items():
        romanized = convert_mora(mora, pronunciation, romanized)

    # 直音の変換
    for group, mapping in chokuon.items():
        for mora, pronunciation in mapping.items():
            romanized = convert_mora(mora, pronunciation, romanized)

    # 促音の変換
    replace = {"(-ッ)(.)": r"\2-\2", "c-ch": "t-ch"}
    for pattern, replacement in replace.items():
        romanized = re.sub(pattern, replacement, romanized)

    # 長音の変換
    moras_before_long_sounds: list = re.findall("([a-z]*)-ー", romanized)
    for mora in moras_before_long_sounds:
        for group, mapping in chokuon.items():
            if mora in mapping.values():
                romanized = re.sub(f"{mora}-ー",
                                   f"{mora}-{chokuon[group][group]}-", romanized)

    # 撥音の処理
    romanized = re.sub("(?<=-)n(?=-[pbm])", "m", romanized)

    # 無声子音処理
    # TODO 情報不足

    # 仕上げ
    romanized = romanized[:-1]

    return romanized


def run_test() -> None:
    ground_truth = {
        "モチカタ": "moh-ch-kah-tah",
        "デス": "deh-ss",
        "カメ": "kah-meh",
        "セート": "seh-eh-toh",
        "ヒョーコー": "hyohh-koh-oh",
        "コッチ": "koht-chee",
        "タップリ": "tahp-poo-ree",
        "ハイッテル": "hah-eet-teh-roo",
        "ハンブン": "hah-m-boo-n",
        "コンバンワ": "koh-m-bah-n-wa",
        "ライト": "rah-ee-toh",
        "ウィンドサーフィン": "wih-n-doh-sah-ah-fih-n",
        "ヴィレッジヴァンガード": "vih-rehj-jee-va-n-gah-ah-doh",
        }
    for katakana_string, truth in ground_truth.items():
        romanized = romanize(katakana_string)
        result = "CORRECT" if romanized == truth else "WRONG"
        print(f"{katakana_string}: {romanized} <= {result}")
   
