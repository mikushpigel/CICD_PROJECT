def call() {
    if (env.SKIP_STAGE != "true") {
        timeout(time: 5, unit: 'MINUTES') {
            waitForQualityGate abortPipeline: true
        }
    } else {
        echo "Skipping Quality Gate stage"
    }
}