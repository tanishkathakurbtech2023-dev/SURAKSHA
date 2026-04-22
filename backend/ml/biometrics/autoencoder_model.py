class AutoencoderProfiler:
    def reconstruction_error(self, session_features: list[float]) -> float:
        if not session_features:
            return 0.0
        clipped = [min(max(v, 0), 1) for v in session_features]
        avg = sum(clipped) / len(clipped)
        return min(sum(abs(v - avg) for v in clipped) / len(clipped), 1.0)


autoencoder_profiler = AutoencoderProfiler()
