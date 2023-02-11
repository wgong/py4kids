2 types of recommendation engines
1) content filtering : 
based on features of items / products

2) collaborative filtering
based on similar user preferences

ratings: 
explicit - like or dislike
implicit - infer 

ALS algorithms: Alternating Least Square
Apache Spark ML implements alternating least squares (ALS) for collaborative filtering, a very popular algorithm for making recommendations.

ALS recommender is a matrix factorization algorithm that uses Alternating Least Squares with Weighted-Lamda-Regularization (ALS-WR). It factors the user to item matrix A into the user-to-feature matrix U and the item-to-feature matrix M: It runs the ALS algorithm in a parallel fashion.  The ALS algorithm should uncover the latent factors that explain the observed user to item ratings and tries to find optimal factor weights to minimize the least squares between predicted and actual ratings.

[ALS Kaggle Competition](https://www.elenacuoco.com/2016/12/22/alternating-least-squares-als-spark-ml/)


# Group the data by "Genre"
markus_ratings.groupBy("Genre").sum("Num_Views").show()

Convert Original Ratings Matrix into Factor Matrices

Latent features

matrix multiplication is fundamental to ALS

