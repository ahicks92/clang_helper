"""Very dependent on my personal setup.  Will not work for others.  Touches a file outside the repo."""

import clang_helper
info = clang_helper.FeatureExtractor("../camlorn_audio_rewrite/openal-soft/include/al/al.h")
efx = clang_helper.FeatureExtractor("../camlorn_audio_rewrite/openal-soft/include/al/efx.h")