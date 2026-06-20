import subprocess

def run(cmd):
    print(f"\n>>> {cmd}\n")
    subprocess.run(cmd, shell=True)

def main():
    try:
        run("docker compose -f Artefakt03/docker-compose.yml up -d")

        run("python -m pytest --alluredir=allure-results")

        run("allure generate allure-results -o allure-report --clean")

        print("\nPIPELINE FINISHED SUCCESSFULLY")

    finally:
        run("docker compose -f Artefakt03/docker-compose.yml down")

if __name__ == "__main__":
    main()