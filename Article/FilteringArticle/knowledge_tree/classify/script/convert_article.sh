type=$1

articles_path=E:/data/knowledge/classify/$type/article_trainset
article_market_path=E:/data/knowledge/classify/$type/article_trainset_market

python E://github/KnowledgableArticle/Article/FilteringArticle/knowledge_tree/classify/script/convert_article.py \
				$articles_path $article_market_path


articles_path=E:/data/knowledge/classify/$type/article_testset
article_market_path=E:/data/knowledge/classify/$type/article_testset_market

python E://github/KnowledgableArticle/Article/FilteringArticle/knowledge_tree/classify/script/convert_article.py \
				$articles_path $article_market_path