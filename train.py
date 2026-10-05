from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_absolute_error
from sklearn.pipeline import Pipeline

import pandas as pd 
import joblib
from app.features import add_features
from app.config import MODEL_PATH



# 1. Load the dataset 
df = pd.read_csv('data/insurance.csv')

# 2. Define the dependent and independent variables 
X = add_features(df)
y = df['annual_premium']

# 3. split the training and testing data 
X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2,random_state=42
)

# 4. develop the model 
model = Pipeline([
    ("scale",StandardScaler()),
    ("model",LinearRegression())
])

# 5. fit the training data in the model 
model.fit(X_train,y_train)

# evaluate the model using r2 score and the mean absolute error 
pred = model.predict(X_test)

print('R2: ',round(r2_score(y_test,pred),2))
print('MAE: ',round(mean_absolute_error(y_test,pred),2))

# 6. use the joblib to dump the model in the file path in artifacts file 
joblib.dump(model,MODEL_PATH)

print(f'MODEL SAVED AT {MODEL_PATH}')