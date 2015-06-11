# SEPLN-TweetLID14

The TweetLID shared task consists in identifying the language or languages in which tweets are written. Focusing on events, and news in the Iberian Peninsula, the main focus of the task is the identification of tweets written in the 5 top languages from the Peninsula (Basque, Catalan, Galician, Spanish, and Portuguese), and English

We will provide the participants of the task with a training corpus that includes approximately 15,000 tweets manually annotated with the language(s). The participants will have a month to develop and tweak their language identification systems from this training corpus. They will have apply their system on the test set afterwards, and submit the output of the system, which will be evaluated and compared to the other participants’ systems.

It is worth noting that some tweets are written in more than one language (e.g., partly in Portuguese, and partly in Galician), and that the language cannot be determined in some cases (e.g., “jajaja”). The corpus also takes into account these specific cases, providing annotations such as “ca+es” (written in Catalan and Spanish), “ca/es” (it can be either Catalan or Spanish, it does not make a difference in this case), “other” (it is written in a language that is not considered in the task), o “und” (when it cannot be determined).


How to use:

You have 3 main programs to execute if you want to prove our system. The first one to create the database, the second one to prove our algorithms
a demo and the last one to estimate the error with cross validation.

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

