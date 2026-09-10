import argparse

from hr_pipeline.pipeline import run_pipeline


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="WA_Fn-UseC_-HR-Employee-Attrition.csv")
    parser.add_argument("--database-url", default="postgresql+psycopg://hr:hr@localhost:5434/hr_pipeline")
    args = parser.parse_args()
    print(run_pipeline(args.source, args.database_url))
