
#run
root='/data/users/jingbo.han/git/mob_autotag/bin'

python $root/get_word_by_adv.py "meizhuang_adv" "美妆"
#python $root/get_word_by_product.py "muying_product" "婴"


#demo test

# 媒体打标签
python tag_by_url.py "house.163.com"
python tag_by_url.py "http://bj.house.163.com/16/0908/08/C0E7G8EP00073SD3.html"

# 广告主打标签
#adid=16701 http://www.njxjxfq.com
python tag_by_url.py "http://www.njxjxfq.com"
# adid=13571   http://www.yourong.cn/
python tag_by_url.py "http://www.yourong.cn"

# 创意打标签
#和广告主打标签 类似

# app打标签
#消灭星星 http://apk.hiapk.com/appinfo/com.brianbaek.popstar
python tag_by_word.py "消灭星星"
python tag_by_url.py "http://apk.hiapk.com/appinfo/com.brianbaek.popstar"

#  智能创意
python desc_by_word.py "中兴"

# 近期
word_clean.py
word_norm.py
re_doc.py
