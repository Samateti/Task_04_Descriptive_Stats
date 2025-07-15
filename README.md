# Research Task 04 – Descriptive Statistics with and without 3rd Party Libraries( Pandas/Polars)

This project explores and compares three methods for calculating descriptive statistics on real-world social media datasets, including Facebook ads, Facebook posts, and Twitter posts. It aims to assess each approach in terms of accuracy, efficiency, and user-friendliness by using:

* Pure Python (without external libraries)
* Pandas
* Polars

## 📁 Dataset

You’ll need the following files locally (not provided in the repo):
- `2024_fb_ads_president_scored_anon.csv`
- `2024_fb_posts_president_scored_anon.csv`
- `2024_tw_posts_president_scored_anon.csv`

---

## ⚙️ Instructions to Run the Code

1. **Install required libraries**  
   Make sure Python 3.8+ is installed, then run:
   pip install pandas polars matplotlib seaborn

2. **Run the scripts to display stats**
   python pure_python_stats.py     
   python pandas_stats.py         
   python polars_stats.py

## reflective questions
1. **Was it a challenge to produce identical results?**
Yes,differences in type inference, null handling, and built-in formulae meant Python, Pandas, and Polars wouldn’t match exactly out of the box. Aligning them required explicit library, consistent numeric casts, and manually replicating Pandas/Polars’ std-dev logic in pure Python. Once standardized, the summaries converged.

2. **Do you find one approach easier or more performant?**
Pandas offers the gentlest learning curve with one-liner summaries , making it easiest for day-to-day work. Polars, leveraging a Rust backend, outperforms Pandas at scale, especially on multi-million-row datasets. Pure Python is most flexible but slowest—best reserved for algorithm practice or tiny files.

3. **If you were coaching a junior data analyst, what approach would you recommend?**
Start with Pandas to learn data-frame concepts and EDA patterns. As data sizes grow and speed matters, introduce Polars for its superior performance and parallelism. Reserve pure Python for interview prep or when you need total control without external dependencies.

4. **Can coding AI like ChatGPT produce recommendations such as template code to jump start each approach?**
Yes, ChatGPT and similar tools excel at generating boilerplate for all three methods, including CSV readers, summary routines, group-by patterns, and plotting code. They can quickly scaffold projects and suggest best practices, saving hours of initial setup.

5. **What default approach do these tools recommend when asked to produce descriptive statistics?**
AI tools typically recommend a straightforward and widely accepted approach that balances ease of understanding with accuracy. They aim to guide users toward clear, beginner-friendly methods for summarizing and understanding data.

6. **Do you agree with these recommendations (why or why not)?**
Yes, I agree with the default approach because it provides a solid starting point for most data analysis tasks. It helps build confidence in interpreting data without overwhelming users, especially those new to the field.
