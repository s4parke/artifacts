# -*- coding: utf-8 -*-
"""Tests for the artifact definitions readers."""

from __future__ import unicode_literals

import os
import unittest

from artifacts import reader
from artifacts import writer

from tests import test_lib


class ArtifactsWriterTest(test_lib.BaseTestCase):
  """Class to test the artifacts writer."""

  def _TestArtifactsConversion(
      self, artifact_reader, artifact_writer, filename):
    """Tests artifacts conversion.

    Args:
      artifact_reader (ArtifactsReader): artifact reader.
      artifact_writer (ArtifactsWriter): artifact writer.
      filename (str): name of the file to convert.
    """
    test_file = self._GetTestFilePath([filename])
    if not os.path.exists(test_file):
      raise unittest.SkipTest('missing test file: {0:s}'.format(filename))

    artifact_definitions = list(artifact_reader.ReadFile(test_file))

    with test_lib.TempDirectory() as temporary_directory:
      output_file = os.path.join(temporary_directory, filename)

      artifact_writer.WriteArtifactsFile(artifact_definitions, output_file)

      converted_artifact_definitions = list(
          artifact_reader.ReadFile(output_file))

    self.assertListEqual(
        [artifact.AsDict() for artifact in artifact_definitions],
        [artifact.AsDict() for artifact in converted_artifact_definitions])

  def testJsonWriter(self):
    """Tests conversion with the JsonArtifactsWriter."""
    artifact_reader = reader.JsonArtifactsReader()
    artifact_writer = writer.JsonArtifactsWriter()
    self._TestArtifactsConversion(
        artifact_reader, artifact_writer, 'definitions.json')

  def testYamlWriter(self):
    """Tests conversion with the YamlArtifactsWriter."""
    artifact_reader = reader.YamlArtifactsReader()
    artifact_writer = writer.YamlArtifactsWriter()
    self._TestArtifactsConversion(
        artifact_reader, artifact_writer, 'definitions.yaml')


if __name__ == '__main__':
  unittest.main()
