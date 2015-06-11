

README:

You have 3 main programs to execute if you want to prove our system. The first one to create the database, the second one to prove our algorithms
a demo and the last one to estimate de error with cross validation.

For further information you can contact to:

    iosu.mendizabal@gmail.com
    daniel.horowitzzz@gmail.com
    jeronicarandell@gmail.com

    

DBTweetSafa.py = Main to create the database of tweets and language code using parse.com and twitter API.
                After creating the database it saves the items of the database in the folder datasets/*with the specific language.


DemoTweetSafa.py = This is the demostration program where you can prove our algorithms of classification.
                    You can execute the program introducing a text and the program is going to output you the class number the algorithms has
                    classificate.

                    0 = English
                    1 = Spanish
                    2 = French
                    3 = Portuguese

                    Example:
                        python DemoTweetSafa 'Esto es un tweet en espanol en el cual la respuesta tendra que ser el numero uno'

                    Output:
                        Language predicted with Lidstone smoothing = 1
                        Language predicted with ranking = 1

TweetSafa.py = This is the program where we execute the cross validation to estimate the error of our classifiers.
