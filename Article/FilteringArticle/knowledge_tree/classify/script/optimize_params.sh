train_type=$1
test_type=$2

train_article_market_path=E:/data/knowledge/classify/$train_type/article_trainset_market
test_article_market_path=E:/data/knowledge/classify/$test_type/article_testset_market
pos_path=E:/data/knowledge/tools/postag
punc_path=E:/data/knowledge/tools/punctuation
klword_path=E:/data/knowledge/tools/knowledgeable_word
logger_path=E:/data/knowledge/classify/cross/optimize_params_performance_$train_type$test_type

python E://github/KnowledgableArticle/Article/FilteringArticle/knowledge_tree/classify/script/optimize_params.py \
				$train_article_market_path $test_article_market_path $pos_path $punc_path $klword_path $logger_path