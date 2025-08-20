import io
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from smartops.utils import show_page_header, SKLEARN_AVAILABLE, MATPLOTLIB_AVAILABLE, TF_AVAILABLE

# ================== TITANIC ==================
def show_titanic_survival():
    st.header("🚢 Titanic Survival Prediction")
    st.markdown("Upload Titanic dataset and predict survival using logistic regression.")

    uploaded_file = st.file_uploader("Upload Titanic dataset (CSV)", type=["csv"], key="titanic_file")
    if uploaded_file is not None:
        try:
            dataset = pd.read_csv(uploaded_file)

            with st.expander("🔍 View Dataset"):
                st.subheader("Dataset Overview")
                st.write(dataset.head())
                st.subheader("Dataset Info")
                buf = io.StringIO()
                dataset.info(buf=buf)
                st.text(buf.getvalue())

            # Visualizations
            st.subheader("📊 Data Visualizations")
            col1, col2 = st.columns(2)
            with col1:
                fig1, ax1 = plt.subplots()
                sns.countplot(data=dataset, x='Sex', hue='Survived', ax=ax1)
                ax1.set_title('Survival by Gender')
                st.pyplot(fig1)

                fig3, ax3 = plt.subplots()
                sns.countplot(data=dataset, x='SibSp', hue='Survived', ax=ax3)
                ax3.set_title('Survival by Siblings/Spouses')
                st.pyplot(fig3)
            with col2:
                fig2, ax2 = plt.subplots()
                sns.countplot(data=dataset, x='Pclass', hue='Survived', ax=ax2)
                ax2.set_title('Survival by Passenger Class')
                st.pyplot(fig2)

                fig4, ax4 = plt.subplots()
                sns.countplot(data=dataset, x='Parch', hue='Survived', ax=ax4)
                ax4.set_title('Survival by Parents/Children')
                st.pyplot(fig4)

            # Preprocessing
            st.subheader("🧹 Data Preprocessing")
            st.write("### Missing Data")
            missing_data = dataset[['Pclass','Sex','Age','SibSp','Parch']].isnull().sum()
            st.bar_chart(missing_data)

            def fill_age(row):
                age = row['Age']
                pclass = row['Pclass']
                if pd.isna(age):
                    return 38 if pclass == 1 else (29 if pclass == 2 else 25)
                return age

            y = dataset['Survived']
            X = dataset[['Pclass','Sex','Age','SibSp','Parch']].copy()
            X['Age'] = X.apply(fill_age, axis=1)
            X = pd.get_dummies(X, columns=['Sex','Pclass','SibSp','Parch'], drop_first=True)

            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            st.subheader("📈 Model Evaluation")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Accuracy", f"{accuracy_score(y_test, y_pred) * 100:.2f}%")
                report = classification_report(y_test, y_pred, output_dict=True)
                st.json(report)
            with col2:
                cm = confusion_matrix(y_test, y_pred)
                fig, ax = plt.subplots()
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
                ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
                ax.set_title('Confusion Matrix')
                st.pyplot(fig)

            st.subheader("🔮 Make a Prediction")
            with st.form("prediction_form"):
                colA, colB = st.columns(2)
                with colA:
                    pclass = st.selectbox("Passenger Class", [1,2,3], index=0)
                    age = st.slider("Age", 1, 100, 25)
                    sex = st.radio("Sex", ["male","female"])
                with colB:
                    sibsp = st.selectbox("Siblings/Spouses Aboard", [0,1,2,3,4,5,8])
                    parch = st.selectbox("Parents/Children Aboard", [0,1,2,3,4,5,6])

                if st.form_submit_button("Predict Survival"):
                    input_data = {'Age': age}
                    for col in X.columns:
                        input_data[col] = 0
                    if f"Sex_{sex}" in input_data:
                        input_data[f"Sex_{sex}"] = 1
                    if f"Pclass_{pclass}" in input_data:
                        input_data[f"Pclass_{pclass}"] = 1
                    if f"SibSp_{sibsp}" in input_data:
                        input_data[f"SibSp_{sibsp}"] = 1
                    if f"Parch_{parch}" in input_data:
                        input_data[f"Parch_{parch}"] = 1
                    input_df = pd.DataFrame([{**{c:0 for c in X.columns}, **input_data}])[X.columns]
                    pred = model.predict(input_df)[0]
                    proba = model.predict_proba(input_df)[0][pred] * 100
                    if pred == 1:
                        st.success(f"🎉 Predicted: SURVIVED with {proba:.1f}% confidence")
                    else:
                        st.error(f"💀 Predicted: DID NOT SURVIVE with {proba:.1f}% confidence")

        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.info("ℹ️ Please upload a Titanic dataset CSV file to get started.")


# ================== CHURN ==================
def show_churn_prediction():
    st.header("📊 Churn Prediction Model")
    st.markdown("Predict customer churn using a neural network model.")
    try:
        dataset_path = os.path.join("data", "Churn_Modelling.csv")
        dataset = pd.read_csv(dataset_path)
        if st.checkbox("Show Dataset Sample"):
            st.dataframe(dataset.head())

        y = dataset["Exited"]
        X = dataset[['CreditScore','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary','Geography','Gender']]

        geo = pd.get_dummies(X["Geography"], drop_first=True, prefix='Geo')
        gender = pd.get_dummies(X["Gender"], drop_first=True, prefix='Gender')
        X = pd.concat([X[['CreditScore','Age','Tenure','Balance','NumOfProducts','HasCrCard','IsActiveMember','EstimatedSalary']], geo, gender], axis=1)

        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        if not TF_AVAILABLE:
            st.error("TensorFlow not installed. Install with: pip install tensorflow")
            return

        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

        model = Sequential()
        model.add(Dense(units=6, input_dim=X_train.shape[1], kernel_initializer='he_uniform', activation='relu'))
        model.add(Dense(units=7, kernel_initializer='he_uniform', activation='relu'))
        model.add(Dense(units=5, kernel_initializer='he_uniform', activation='relu'))
        model.add(Dense(units=1, kernel_initializer='glorot_uniform', activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        epochs = st.sidebar.slider("Number of Epochs", 1, 50, 10)
        batch_size = st.sidebar.selectbox("Batch Size", [16,32,64], index=1)

        if st.button("🚀 Train Model"):
            with st.spinner("Training the model..."):
                history = model.fit(X_train, y_train, validation_split=0.2, batch_size=batch_size, epochs=epochs, verbose=0)
                y_pred = (model.predict(X_test) > 0.5).astype(int)
                st.success("✅ Model training completed!")
                acc = accuracy_score(y_test, y_pred)
                st.metric("Test Accuracy", f"{acc*100:.2f}%")

                st.subheader("📊 Classification Report")
                report = classification_report(y_test, y_pred, output_dict=True)
                st.json(report)

                st.subheader("📈 Confusion Matrix")
                cm = confusion_matrix(y_test, y_pred)
                fig, ax = plt.subplots()
                sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
                ax.set_xlabel('Predicted'); ax.set_ylabel('Actual'); ax.set_title('Confusion Matrix')
                st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Make sure data/Churn_Modelling.csv exists.")


# ================== SALARY PREDICTION ==================
def show_salary_prediction():
    st.header("💰 Salary Prediction")
    st.markdown("Upload a CSV with features and a 'Salary' column.")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], key="salary_file")
    if uploaded_file is not None:
        try:
            dataset = pd.read_csv(uploaded_file)
            st.subheader("Dataset Preview")
            st.dataframe(dataset.head())

            if 'Salary' not in dataset.columns:
                st.error("CSV must have a 'Salary' column")
                return

            y = dataset['Salary']
            X = dataset.drop(columns=['Salary'])

            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import mean_squared_error, r2_score

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            st.subheader("📈 Model Performance")
            st.write(f"R² Score: {r2_score(y_test, y_pred):.2f}")
            st.write(f"Mean Squared Error: {mean_squared_error(y_test, y_pred):.2f}")

            st.subheader("🔮 Make a Prediction")
            with st.form("salary_predict_form"):
                input_data = {}
                for col in X.columns:
                    input_data[col] = st.number_input(f"{col}", value=float(dataset[col].mean()))
                if st.form_submit_button("Predict Salary"):
                    input_df = pd.DataFrame([input_data])
                    pred_salary = model.predict(input_df)[0]
                    st.success(f"💰 Predicted Salary: {pred_salary:.2f}")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


# ================== MAIN ==================
def show_machine_learning():
    show_page_header("🤖 Machine Learning Tools")

    if not SKLEARN_AVAILABLE:
        st.error("⚠️ scikit-learn is required. Install: pip install scikit-learn")
        return
    if not MATPLOTLIB_AVAILABLE:
        st.warning("⚠️ matplotlib/seaborn missing. Install: pip install matplotlib seaborn")

    tab1, tab2, tab3 = st.tabs(["🚢 Titanic Survival", "📊 Churn Prediction", "💰 Salary Prediction"])
    with tab1:
        show_titanic_survival()
    with tab2:
        show_churn_prediction()
    with tab3:
        show_salary_prediction()
