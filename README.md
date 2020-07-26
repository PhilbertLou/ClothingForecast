<h3>Brief Overview:</h3>
Welcome to Clothing Forecast (formerly known as WeatherWear), a program to help you decide what to wear on a given day! This web app uses TensorFlow to create a neural network that learns what clothing combinations should be worn on which temperature and weather conditions and can be trained to your personal preference.

More features coming soon!

Full external documentation on how to use this can be found on the site: <a href="http://philbert.pythonanywhere.com/users/ClothingForecast">Click here</a>
<br>(This will bring you to the homepage, which gives a brief overview of the application in further detail. The user's guide can be accessed through the nav bar.)

<h3>Technologies</h3>
Backend: <strong/>Django framework</strong> is used to overall construct this web application. The default Django user/admin/auth is used to make and control user accounts. All information related to a user is stored in a <strong>SQLite</strong> database (the table is based on a custom model). In the application side of this project, <strong>TensorFlow</strong> libraries are used to construct a neural network. This takes the supervised machine learning approach as it is fed 7000 samples of data and its results, and is loosely trained to 'general preferences' in different weather conditions. More information is trained into the existing neural network, resulting in more personalized results as the user continues to use this web application. <strong><a href="https://openweathermap.org/">Openweatherapi</a></strong> is used to fetch the current weather data that will be used for predictions. When the user is logged out, their information is stored using <strong><a href="https://cloud.google.com/storage">Google Cloud Storage</a></strong>, and retrieved from there to be used when they log in.    
<br><br>
Frontend: <strong>Boostrap</strong>, a CSS framework, is used to style the webpage in an aesthetically pleasing way and also to make the components responsive. <strong>Django's templating language</strong> made it simple to create a dynamic webpage that will display certain information when certain conditions are met. 


<br><br>
Edit 07/07/20: The ML part is finished, code is cleaned up and the old stuff can be found in folders that indicate the old files. WeatherWear1.0 and WeatherWearTrainer1 are the most updated versions, using information from WeatherWear folder.

Edit 17/07/20: All functions have been put on a functional website and can be found in the Ver 1.2 Githubver folder.

Edit 26/07/20: Final deployment files can be found in the deployment files folder. This is the final and updated version of the previously uploaded file.
