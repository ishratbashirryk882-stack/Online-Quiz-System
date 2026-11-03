
import streamlit as st

st.title("🎓 Online Quiz Management System")

# 👨‍💻 Admin Panel
menu = st.sidebar.selectbox(
    "📌 Select Menu",
    ["👨‍💻 Admin Panel", "📝 Student Panel", "📊 View Results"]
)


# 👨‍💻 ADMIN PANEL
if menu == "👨‍💻 Admin Panel":

    st.header("➕ Add Questions")

    statement = st.text_input("❓ Enter Question")

    a = st.text_input("🅰️ Option A")
    b = st.text_input("🅱️ Option B")
    c = st.text_input("©️ Option C")
    d = st.text_input("🅳 Option D")

    correct = st.selectbox(
        "✅ Correct Answer",
        ["A", "B", "C", "D"]
    )

    if st.button("💾 Save Question"):

        if statement and a and b and c and d:

            file = open("questions.txt", "a")

            file.write(statement + "\n")
            file.write(a + "\n")
            file.write(b + "\n")
            file.write(c + "\n")
            file.write(d + "\n")
            file.write(correct + "\n")

            file.close()

            st.success("🎉 Question Saved Successfully!")

        else:
            st.warning("⚠️ Fill All Fields")

    st.subheader("📚 Available Questions")

    if "questions" not in st.session_state:
        st.session_state.questions = []

    file = open("questions.txt", "r") if False else None

    try:
        file = open("questions.txt", "r")

        i = 1

        while True:
            question = file.readline()

            if not question:
                break

            st.write("❓ " + str(i) + ". " + question.strip())

            file.readline()
            file.readline()
            file.readline()
            file.readline()
            file.readline()

            i = i + 1

        file.close()

    except FileNotFoundError:
        st.info("📭 No Questions Available")


# 📝 STUDENT PANEL
elif menu == "📝 Student Panel":

    st.header("🎯 Attempt Quiz")

    name = st.text_input("👤 Enter Your Name")

    if st.button("🚀 Start Quiz"):

        st.session_state.start = True

    if "start" in st.session_state:

        file = open("questions.txt", "r")

        questions = []

        while True:

            question = file.readline()

            if not question:
                break

            a = file.readline()
            b = file.readline()
            c = file.readline()
            d = file.readline()
            correct = file.readline()

            questions.append([
                question.strip(),
                a.strip(),
                b.strip(),
                c.strip(),
                d.strip(),
                correct.strip()
            ])

        file.close()

        if len(questions) == 0:

            st.warning("⚠️ No Questions Available")

        else:

            with st.form("quiz_form"):

                answers = []

                i = 0

                for q in questions:

                    st.write("❓ Question", i + 1)
                    st.write(q[0])

                    answer = st.radio(
                        "👇 Select Answer",
                        [
                            "🅰️ A) " + q[1],
                            "🅱️ B) " + q[2],
                            "©️ C) " + q[3],
                            "🅳 D) " + q[4]
                        ],
                        key=i
                    )

                    answers.append(answer.split(")")[0][-1])

                    i = i + 1

                submit = st.form_submit_button("✅ Submit Quiz")

            if submit:

                if name:

                    score = 0
                    i = 0

                    for q in questions:

                        if answers[i] == q[5]:
                            score = score + 1

                        i = i + 1

                    total = len(questions)

                    st.success("🎉 Quiz Submitted!")

                    st.write("👤 Student Name:", name)
                    st.write("🏆 Your Score:", score, "/", total)

                    if score >= total / 2:
                        st.success("🎊 You Passed!")
                    else:
                        st.error("😔 You Failed!")

                    file = open("results.txt", "a")

                    file.write(name + "\n")
                    file.write(str(score) + "\n")
                    file.write(str(total) + "\n")

                    file.close()

                else:
                    st.warning("⚠️ Enter Your Name")


# 📊 VIEW RESULTS
elif menu == "📊 View Results":

    st.header("🏆 Student Results")

    search_name = st.text_input("🔍 Search Student Name")

    if st.button("🔎 Search Results"):

        try:

            file = open("results.txt", "r")

            found = False

            while True:

                name = file.readline()

                if not name:
                    break

                score = file.readline()
                total = file.readline()

                if search_name.lower() in name.strip().lower():

                    st.write("👤 Student Name:", name.strip())
                    st.write("🏆 Score:", score.strip(), "/", total.strip())

                    found = True

            file.close()

            if not found:
                st.warning("🔍 No Result Found")

        except FileNotFoundError:
            st.warning("📭 No Results Available")
