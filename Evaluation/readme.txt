# EVALUATION:

# PARA USAR EL tweetLID_eval.pl TENEMOS QUE CREAR UN FICHERO EN EL QUE LOS TWEETS ESTEN DE LA SIGUIENTE MANERA:

#   tweet_id<TAB>language
#
#   HE PUESTO UN EJEMPLO COGIENDO TWEETS DE OUTPUT_COMPLETE LOS HE GUARDADO EN EL FICHERO result.txt
#
#   Para probar el codigo ejecutar la siguiente linea:
#
#    perl tweetLID_eval.pl -d ../Results/resultLinearInterpolation.txt -r ../Dataset/output_complete.txt ->../Evaluation/evaluation_ouput_linear.txt
#
#   LO QUE HACE ESTA LINEA ES MIRAR EL RESULT.TXT CREADO POR NOSOTROS, COMPARARLO CON EL OUTPUT_COMPLETE.TXT Y GUARDAR LOS
#       RESULTADOS EN EL EVALUATION_OUTPUT.TXT
#
#   AHI ESTA TODA LA INFORMACION DE LA PRECISION RECAL ETC... EXPLICADA.