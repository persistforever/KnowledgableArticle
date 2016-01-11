type=$1

article_market_path=E:/data/knowledge/classify/$type/article_trainset_market
feature_path=E:/data/knowledge/classify/$type/trainset_feature
feature_market_path=E:/data/knowledge/classify/$type/trainset_feature_market
pos_path=E:/data/knowledge/tools/postag
punc_path=E:/data/knowledge/tools/punctuation
klword_path=E:/data/knowledge/tools/knowledgeable_word

python E://github/KnowledgableArticle/Article/FilteringArticle/knowledge_tree/classify/script/feature_select.py \
				$article_market_path $feature_path $feature_market_path $pos_path $punc_path $klword_path

				
article_market_path=E:/data/knowledge/classify/$type/article_testset_market
feature_path=E:/data/knowledge/classify/$type/testset_feature
feature_market_path=E:/data/knowledge/classify/$type/testset_feature_market

python E://github/KnowledgableArticle/Article/FilteringArticle/knowledge_tree/classify/script/feature_select.py \
				$article_market_path $feature_path $feature_market_path $pos_path $punc_path $klword_path