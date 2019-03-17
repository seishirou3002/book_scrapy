{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "doujin_scrap.ipynb",
      "version": "0.3.2",
      "provenance": [],
      "collapsed_sections": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/seishirou3002/book_scrapy/blob/master/doujin_scrap.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "metadata": {
        "id": "KZExtJtQT3s8",
        "colab_type": "code",
        "outputId": "f635eb90-2a2b-421d-cb7f-b297691d430b",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 831
        }
      },
      "cell_type": "code",
      "source": [
        "#画像とタイトルとサークルを取得する\n",
        "#http://doujinantena.com/list.php?category=update\n",
        "#上記のURLを取得する\n",
        "#----------ここから-------------------------\n",
        "#divタグのclass=listtype-aを取得する\n",
        "#次のページのリンクも取得\n",
        "#欲しい情報ごとに分類する（画像 タイトル サークル） imgタグのsrc class=\"booktitle\"  class=\"circle\"\n",
        "#上記の3つのタグの情報を取得する\n",
        "#----------ここまで-------------------------\n",
        "#画像については要調査\n",
        "#1ページを終えたら次のページ\n",
        "#ページ遷移がなくなるまで繰り返す\n",
        "#3つの情報をexcelに書き込む\n",
        "#毎日AM1:00に実行する\n",
        "from bs4 import BeautifulSoup\n",
        "import requests\n",
        "import openpyxl as px\n",
        "import time\n",
        "from urllib.parse import urljoin\n",
        "import numpy as np\n",
        "\n",
        "#ページ遷移が終わるまでタイトルと画像とサークル名を取得する\n",
        "def getScrapList():\n",
        "  #取得するリストを用意\n",
        "  img_list = []\n",
        "  title_list = []\n",
        "  circle_list = []\n",
        "  \n",
        "  #ベースになるアドレス\n",
        "  base_url = \"http://doujinantena.com/\"\n",
        "  dynamic_url = \"http://doujinantena.com/list.php?category=update\" #初期URL\n",
        "  \n",
        "  while True:\n",
        "    \n",
        "    #指定したURLのhtmlを取得する\n",
        "    res = requests.get(dynamic_url)\n",
        "    res.raise_for_status() # エラー処理\n",
        "    html = BeautifulSoup(res.content,\"html.parser\")\n",
        "    \n",
        "    #次のページのURLを取得する\n",
        "    next_page = html.find(class_=\"nex\")\n",
        "  \n",
        "    #divタグのclass=listtype-aタグ内のliタグを取得する\n",
        "    tag_li_list = html.select('.listtype-a > ul > li')\n",
        "  \n",
        " \n",
        " \n",
        "    #取得したタグから3つの情報をリストに格納する\n",
        "    for li in tag_li_list:\n",
        "    \n",
        "      #img srcタグのurlをリストに格納\n",
        "      tmp = li.find('img')\n",
        "      img_list.append(tmp['src'])\n",
        "    \n",
        "      #titleをリストに格納\n",
        "      tmp = li.find(class_=\"booktitle\")\n",
        "      title_list.append(tmp.string)\n",
        "    \n",
        "      #circleをリストに格納\n",
        "      tmp = li.find(class_=\"circle\")\n",
        "      #get_text()でタグ内のテキストを抜き出す、邪魔なサークル：をreplace()で削除\n",
        "      circle_list.append(tmp.get_text().replace(\"サークル：\",\"\"))\n",
        "    \n",
        "    #次のページのアドレスがない場合終了する\n",
        "    if bool(next_page) == False:\n",
        "      break\n",
        "    \n",
        "    dynamic_url = urljoin(base_url, next_page.a.get(\"href\"))\n",
        "    time.sleep(5)\n",
        "  #print(next_page)\n",
        "  print(\"読み込み完了\")\n",
        "  return img_list,title_list,circle_list  \n",
        "\n",
        "#３つの配列を行列に変換\n",
        "def reshape_array(img_list,title_list,circle_list):\n",
        "  np_img = np.array(img_list)\n",
        "  np_title = np.array(title_list)\n",
        "  np_circle = np.array(circle_list)\n",
        "  \n",
        "  np_list = np.hstack((np_img.reshape(len(np_img),1),np_title.reshape(len(np_title),1),np_circle.reshape(len(np_circle),1)))\n",
        "  print(\"変換完了\")\n",
        "  list = np_list.tolist()\n",
        "  return list\n",
        "\n",
        "#画像とタイトルとサークル名をexcelに記載する\n",
        "def write_excel(list,path):\n",
        "  \n",
        "    wb = px.Workbook()\n",
        "    wb.save(path)\n",
        "    ws = wb.active\n",
        "    \n",
        "    colum_head = [\"画像\",\"タイトル\",\"サークル名\"]\n",
        "    rows = []\n",
        "    rows.append(colum_head)\n",
        "    rows.append(list)\n",
        "    \n",
        "    #全行分\n",
        "    for row in rows:\n",
        "      ws.append(row)\n",
        "        \n",
        "    \n",
        "    print(\"ファイル作成完了\")\n",
        "    \n",
        "[img,title,circle] = getScrapList()\n",
        "list = reshape_array(img,title,circle)\n",
        "write_excel(list,\"C:\\work\\python\\20190301_scrap_practice\\doujin_result.xlsx\")"
      ],
      "execution_count": 8,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "読み込み完了\n",
            "変換完了\n"
          ],
          "name": "stdout"
        },
        {
          "output_type": "error",
          "ename": "ValueError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mValueError\u001b[0m                                Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-8-511ddf9c7804>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m()\u001b[0m\n\u001b[1;32m     89\u001b[0m \u001b[0;34m[\u001b[0m\u001b[0mimg\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mtitle\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mcircle\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mgetScrapList\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     90\u001b[0m \u001b[0mlist\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mreshape_array\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mimg\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mtitle\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mcircle\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 91\u001b[0;31m \u001b[0mwrite_excel\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mlist\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\"C:\\work\\python\\20190301_scrap_practice\\doujin_result.xlsx\"\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
            "\u001b[0;32m<ipython-input-8-511ddf9c7804>\u001b[0m in \u001b[0;36mwrite_excel\u001b[0;34m(list, path)\u001b[0m\n\u001b[1;32m     82\u001b[0m     \u001b[0;31m#全行分\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     83\u001b[0m     \u001b[0;32mfor\u001b[0m \u001b[0mrow\u001b[0m \u001b[0;32min\u001b[0m \u001b[0mrows\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 84\u001b[0;31m       \u001b[0mws\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mappend\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mrow\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     85\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     86\u001b[0m     \u001b[0mwb\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msave\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.6/dist-packages/openpyxl/worksheet/worksheet.py\u001b[0m in \u001b[0;36mappend\u001b[0;34m(self, iterable)\u001b[0m\n\u001b[1;32m    775\u001b[0m                     \u001b[0mcell\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrow\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mrow_idx\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    776\u001b[0m                 \u001b[0;32melse\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 777\u001b[0;31m                     \u001b[0mcell\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mCell\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mrow\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mrow_idx\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcol_idx\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mcol_idx\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mcontent\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    778\u001b[0m                 \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_cells\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mrow_idx\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mcol_idx\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mcell\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    779\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.6/dist-packages/openpyxl/cell/cell.py\u001b[0m in \u001b[0;36m__init__\u001b[0;34m(self, worksheet, column, row, value, col_idx, style_array)\u001b[0m\n\u001b[1;32m    113\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdata_type\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m'n'\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    114\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mvalue\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 115\u001b[0;31m             \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mvalue\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    116\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_comment\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    117\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0mcolumn\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.6/dist-packages/openpyxl/cell/cell.py\u001b[0m in \u001b[0;36mvalue\u001b[0;34m(self, value)\u001b[0m\n\u001b[1;32m    292\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    293\u001b[0m         \u001b[0;34m\"\"\"Set the value and infer type and display options.\"\"\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 294\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_bind_value\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    295\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    296\u001b[0m     \u001b[0;34m@\u001b[0m\u001b[0mproperty\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.6/dist-packages/openpyxl/cell/cell.py\u001b[0m in \u001b[0;36m_bind_value\u001b[0;34m(self, value)\u001b[0m\n\u001b[1;32m    205\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    206\u001b[0m         \u001b[0;32melif\u001b[0m \u001b[0mvalue\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 207\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mValueError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"Cannot convert {0!r} to Excel\"\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    208\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    209\u001b[0m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_value\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mValueError\u001b[0m: Cannot convert ['http://cdn.doujinantena.com/thumbnail/65cf9e395729adb7ec89ada0edf9cca0.jpg', 'アローラの夜のすがた３', 'DOLL PLAY'] to Excel"
          ]
        }
      ]
    },
    {
      "metadata": {
        "id": "MXnH-Q3QgXtj",
        "colab_type": "code",
        "colab": {}
      },
      "cell_type": "code",
      "source": [
        ""
      ],
      "execution_count": 0,
      "outputs": []
    }
  ]
}