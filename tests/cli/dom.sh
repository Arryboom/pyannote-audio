#!/usr/bin/env bash

export PYANNOTE_DATABASE_CONFIG=$GITHUB_WORKSPACE/tests/data/database.yml
export DEBUG=Debug.SpeakerDiarization.Debug
pyannote-audio train --to=2 $GITHUB_WORKSPACE/tests/cli/dom $DEBUG
pyannote-audio validate --subset=train --to=last $GITHUB_WORKSPACE/tests/cli/dom/train/$DEBUG.train $DEBUG
pyannote-audio apply $GITHUB_WORKSPACE/tests/cli/dom/train/$DEBUG.train/validate_accuracy/$DEBUG.train $DEBUG
