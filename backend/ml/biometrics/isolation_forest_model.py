from statistics import mean


class IsolationForestProfiler:
    def anomaly_score(self, session_features: list[float]) -> float:
        if not session_features:
            return 0.0
        baseline = mean(session_features)
        return min(abs(baseline - 0.5) * 2, 1.0)


isolation_forest_profiler = IsolationForestProfiler()
