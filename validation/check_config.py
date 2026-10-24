
import os
import sys

ALLOWED_ENVIRONMENTS = {
    "development",
    "test",
    "production",
}

#This will check Env is among dev,test,prod and through error if its other than this.
#This check will block github action workflow if failure occurs
def main() -> int:
    app_env = os.getenv("APP_ENV", "development").strip().lower()

    if app_env not in ALLOWED_ENVIRONMENTS:
        print(
            f"ERROR: Invalid APP_ENV '{app_env}'. "
            f"Allowed values: {', '.join(sorted(ALLOWED_ENVIRONMENTS))}"
        )
        return 1

    print(f"Configuration validation passed: APP_ENV={app_env}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
