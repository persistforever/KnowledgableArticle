train_type=$1
test_type=$2


train_path=E:/data/knowledge/classify/$train_type/trainset_feature_market
test_path=E:/data/knowledge/classify/$test_type/testset_feature_market

python E://github/KnowledgableArticle/Article/FilteringArticle/knowledge_tree/classify/script/classifying.py \
				$train_path $test_path