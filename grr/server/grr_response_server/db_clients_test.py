#!/usr/bin/env python
# -*- mode: python; encoding: utf-8 -*-
from grr.lib import rdfvalue
from grr.lib import utils
from grr.lib.rdfvalues import client as rdf_client
from grr.lib.rdfvalues import crypto
from grr.lib.rdfvalues import objects
from grr.server.grr_response_server import db

CERT = crypto.RDFX509Cert("""-----BEGIN CERTIFICATE-----
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
-----END CERTIFICATE-----""")


class DatabaseTestClientsMixin(object):
  """An abstract class for testing db.Database implementations.

  This mixin adds methods to test the handling of client data.
  """

  def _InitializeClient(self, client_id):
    self.db.WriteClientMetadata(client_id, fleetspeak_enabled=True)

  def testClientWriteToUnknownClient(self):
    d = self.db
    client_id = "C.fc413187fefa1dcf"

    with self.assertRaises(db.UnknownClientError):
      d.WriteClientSnapshot(objects.ClientSnapshot(client_id=client_id))

  def testKeywordWriteToUnknownClient(self):
    d = self.db
    client_id = "C.fc413187fefa1dcf"

    with self.assertRaises(db.UnknownClientError):
      d.AddClientKeywords(client_id, ["keyword"])

    d.RemoveClientKeyword(client_id, "test")

  def testLabelWriteToUnknownClient(self):
    d = self.db
    client_id = "C.fc413187fefa1dcf"

    with self.assertRaises(db.UnknownClientError):
      d.AddClientLabels(client_id, "testowner", ["label"])

    d.RemoveClientLabels(client_id, "testowner", ["label"])

  def testClientMetadataInitialWrite(self):
    d = self.db

    client_id_1 = "C.fc413187fefa1dcf"
    # Typical initial FS enabled write
    d.WriteClientMetadata(client_id_1, fleetspeak_enabled=True)

    client_id_2 = "C.00413187fefa1dcf"
    # Typical initial non-FS write
    d.WriteClientMetadata(
        client_id_2,
        certificate=CERT,
        first_seen=rdfvalue.RDFDatetime(100000000),
        fleetspeak_enabled=False)

    res = d.MultiReadClientMetadata([client_id_1, client_id_2])
    self.assertEqual(len(res), 2)

    m1 = res[client_id_1]
    self.assertIsInstance(m1, objects.ClientMetadata)
    self.assertTrue(m1.fleetspeak_enabled)

    m2 = res[client_id_2]
    self.assertIsInstance(m2, objects.ClientMetadata)
    self.assertFalse(m2.fleetspeak_enabled)
    self.assertEqual(m2.certificate, CERT)
    self.assertEqual(m2.first_seen, rdfvalue.RDFDatetime(100000000))

  def testClientMetadataSubsecond(self):
    client_id = "C.fc413187fefa1dcf"
    self.db.WriteClientMetadata(
        client_id,
        certificate=CERT,
        first_seen=rdfvalue.RDFDatetime(100000001),
        last_clock=rdfvalue.RDFDatetime(100000011),
        last_foreman=rdfvalue.RDFDatetime(100000021),
        last_ping=rdfvalue.RDFDatetime(100000031),
        fleetspeak_enabled=False)
    res = self.db.MultiReadClientMetadata([client_id])
    self.assertEqual(len(res), 1)
    m1 = res[client_id]
    self.assertEqual(m1.first_seen, rdfvalue.RDFDatetime(100000001))
    self.assertEqual(m1.clock, rdfvalue.RDFDatetime(100000011))
    self.assertEqual(m1.last_foreman_time, rdfvalue.RDFDatetime(100000021))
    self.assertEqual(m1.ping, rdfvalue.RDFDatetime(100000031))

  def testClientMetadataPing(self):
    d = self.db

    client_id_1 = "C.fc413187fefa1dcf"
    self._InitializeClient(client_id_1)

    # Typical update on client ping.
    d.WriteClientMetadata(
        client_id_1,
        last_ping=rdfvalue.RDFDatetime(200000000000),
        last_clock=rdfvalue.RDFDatetime(210000000000),
        last_ip=rdf_client.NetworkAddress(human_readable_address="8.8.8.8"),
        last_foreman=rdfvalue.RDFDatetime(220000000000))

    res = d.MultiReadClientMetadata([client_id_1])
    self.assertEqual(len(res), 1)
    m1 = res[client_id_1]
    self.assertIsInstance(m1, objects.ClientMetadata)
    self.assertTrue(m1.fleetspeak_enabled)
    self.assertEqual(m1.ping, rdfvalue.RDFDatetime(200000000000))
    self.assertEqual(m1.clock, rdfvalue.RDFDatetime(210000000000))
    self.assertEqual(
        m1.ip, rdf_client.NetworkAddress(human_readable_address="8.8.8.8"))
    self.assertEqual(m1.last_foreman_time, rdfvalue.RDFDatetime(220000000000))

  def testClientMetadataValidatesIP(self):
    d = self.db
    client_id = "C.fc413187fefa1dcf"
    with self.assertRaises(TypeError):
      d.WriteClientMetadata(
          client_id, fleetspeak_enabled=True, last_ip="127.0.0.1")

  def testReadAllClientIDsEmpty(self):
    result = list(self.db.ReadAllClientIDs())
    self.assertItemsEqual(result, [])

  def testReadAllClientIDsSome(self):
    self._InitializeClient("C.aaaaaaaaaaaaaaaa")
    self._InitializeClient("C.bbbbbbbbbbbbbbbb")
    self._InitializeClient("C.cccccccccccccccc")

    result = list(self.db.ReadAllClientIDs())
    self.assertItemsEqual(result, [
        "C.aaaaaaaaaaaaaaaa",
        "C.bbbbbbbbbbbbbbbb",
        "C.cccccccccccccccc",
    ])

  def _SetUpReadClientSnapshotHistoryTest(self):
    d = self.db

    self.client_id = "C.fc413187fefa1dcf"
    self._InitializeClient(self.client_id)

    timestamps = [rdfvalue.RDFDatetime.Now()]

    client = objects.ClientSnapshot(client_id=self.client_id, kernel="12.3")
    client.knowledge_base.fqdn = "test1234.examples.com"
    d.WriteClientSnapshot(client)
    timestamps.append(d.ReadClientSnapshot(self.client_id).timestamp)

    timestamps.append(rdfvalue.RDFDatetime.Now())

    client.kernel = "12.4"
    d.WriteClientSnapshot(client)
    timestamps.append(d.ReadClientSnapshot(self.client_id).timestamp)

    timestamps.append(rdfvalue.RDFDatetime.Now())

    return timestamps

  def testReadClientSnapshotHistory(self):
    d = self.db

    self._SetUpReadClientSnapshotHistoryTest()

    hist = d.ReadClientSnapshotHistory(self.client_id)
    self.assertEqual(len(hist), 2)
    self.assertIsInstance(hist[0], objects.ClientSnapshot)
    self.assertIsInstance(hist[1], objects.ClientSnapshot)
    self.assertGreater(hist[0].timestamp, hist[1].timestamp)
    self.assertIsInstance(hist[0].timestamp, rdfvalue.RDFDatetime)
    self.assertEqual(hist[0].kernel, "12.4")
    self.assertEqual(hist[1].kernel, "12.3")

  def testReadClientSnapshotHistoryWithEmptyTimerange(self):
    d = self.db

    self._SetUpReadClientSnapshotHistoryTest()

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(None, None))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].kernel, "12.4")
    self.assertEqual(hist[1].kernel, "12.3")

  def testReadClientSnapshotHistoryWithTimerangeWithBothFromTo(self):
    d = self.db

    ts = self._SetUpReadClientSnapshotHistoryTest()

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[0], ts[2]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].kernel, "12.3")

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[2], ts[4]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].kernel, "12.4")

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[0], ts[4]))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].kernel, "12.4")
    self.assertEqual(hist[1].kernel, "12.3")

  def testReadClientSnapshotHistoryWithTimerangeWithFromOnly(self):
    d = self.db

    ts = self._SetUpReadClientSnapshotHistoryTest()

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[0], None))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].kernel, "12.4")
    self.assertEqual(hist[1].kernel, "12.3")

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[2], None))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].kernel, "12.4")

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[4], None))
    self.assertEqual(len(hist), 0)

  def testReadClientSnapshotHistoryWithTimerangeWithToOnly(self):
    d = self.db

    ts = self._SetUpReadClientSnapshotHistoryTest()

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(None, ts[0]))
    self.assertEqual(len(hist), 0)

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(None, ts[2]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].kernel, "12.3")

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(None, ts[4]))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].kernel, "12.4")
    self.assertEqual(hist[1].kernel, "12.3")

  def testReadClientSnapshotHistoryWithTimerangeEdgeCases(self):
    # Timerange should work as [from, to]. I.e. "from" is inclusive and "to"
    # is inclusive.

    d = self.db

    ts = self._SetUpReadClientSnapshotHistoryTest()

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[1], ts[1]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].kernel, "12.3")

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[1], ts[2]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].kernel, "12.3")

    hist = d.ReadClientSnapshotHistory(self.client_id, timerange=(ts[1], ts[3]))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].kernel, "12.4")
    self.assertEqual(hist[1].kernel, "12.3")

  def testWriteClientSnapshotHistory(self):
    client_id = "C.0000000000000000"
    self._InitializeClient(client_id)

    client_a = objects.ClientSnapshot(client_id=client_id)
    client_a.kernel = "1.2.3"
    client_a.startup_info.client_info.client_version = 42
    client_a.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2010-01-01")

    client_b = objects.ClientSnapshot(client_id=client_id)
    client_b.kernel = "4.5.6"
    client_b.startup_info.client_info.client_version = 108
    client_b.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2010-02-01")

    client_c = objects.ClientSnapshot(client_id=client_id)
    client_c.kernel = "7.8.9"
    client_c.startup_info.client_info.client_version = 707
    client_c.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2010-03-01")

    self.db.WriteClientSnapshotHistory([client_a, client_b, client_c])

    # Check whether the client history has been recorded correctly.
    history = self.db.ReadClientSnapshotHistory(client_id)
    self.assertEqual(len(history), 3)

    self.assertEqual(history[0].kernel, "7.8.9")
    self.assertEqual(history[0].startup_info.client_info.client_version, 707)
    self.assertEqual(history[0].timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-03-01"))

    self.assertEqual(history[1].kernel, "4.5.6")
    self.assertEqual(history[1].startup_info.client_info.client_version, 108)
    self.assertEqual(history[1].timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-02-01"))

    self.assertEqual(history[2].kernel, "1.2.3")
    self.assertEqual(history[2].startup_info.client_info.client_version, 42)
    self.assertEqual(history[2].timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-01-01"))

    # Check whether the snapshot history has been recorded correctly.
    history = self.db.ReadClientStartupInfoHistory(client_id)
    self.assertEqual(len(history), 3)

    self.assertEqual(history[0].client_info.client_version, 707)
    self.assertEqual(history[0].timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-03-01"))

    self.assertEqual(history[1].client_info.client_version, 108)
    self.assertEqual(history[1].timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-02-01"))

    self.assertEqual(history[2].client_info.client_version, 42)
    self.assertEqual(history[2].timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-01-01"))

  def testWriteClientSnapshotHistoryUpdatesLastTimestampIfNotSet(self):
    client_id = "C.0000000000000000"
    self._InitializeClient(client_id)

    client_new = objects.ClientSnapshot(client_id=client_id)
    client_new.kernel = "1.0.0"
    client_new.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2010-01-01")
    self.db.WriteClientSnapshotHistory([client_new])

    info = self.db.ReadClientFullInfo(client_id)
    self.assertEqual(info.last_snapshot.kernel, "1.0.0")
    self.assertEqual(info.last_snapshot.timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-01-01"))
    self.assertEqual(info.last_startup_info.timestamp,
                     rdfvalue.RDFDatetime.FromHumanReadable("2010-01-01"))

  def testWriteClientSnapshotHistoryUpdatesLastTimestampIfNewer(self):
    client_id = "C.0000000000000000"
    self._InitializeClient(client_id)

    client_old = objects.ClientSnapshot(client_id=client_id)
    client_old.kernel = "1.0.0"
    self.db.WriteClientSnapshot(client_old)

    old_timestamp = self.db.ReadClientSnapshot(client_id).timestamp

    client_new = objects.ClientSnapshot(client_id=client_id)
    client_new.kernel = "2.0.0"
    client_new.timestamp = rdfvalue.RDFDatetime.Now()
    self.db.WriteClientSnapshotHistory([client_new])

    info = self.db.ReadClientFullInfo(client_id)
    self.assertEqual(info.last_snapshot.kernel, "2.0.0")
    self.assertGreater(info.last_snapshot.timestamp, old_timestamp)
    self.assertGreater(info.last_startup_info.timestamp, old_timestamp)

  def testWriteClientSnapshotHistoryDoesNotUpdateLastTimestampIfOlder(self):
    client_id = "C.0000000000000000"
    self._InitializeClient(client_id)

    client_new = objects.ClientSnapshot(client_id=client_id)
    client_new.kernel = "2.0.0"
    self.db.WriteClientSnapshot(client_new)

    new_timestamp = self.db.ReadClientSnapshot(client_id).timestamp

    client_old = objects.ClientSnapshot(client_id=client_id)
    client_old.kernel = "1.0.0"
    client_old.timestamp = new_timestamp - rdfvalue.Duration("1d")
    self.db.WriteClientSnapshotHistory([client_old])

    info = self.db.ReadClientFullInfo(client_id)
    self.assertEqual(info.last_snapshot.kernel, "2.0.0")
    self.assertEqual(info.last_snapshot.timestamp, new_timestamp)
    self.assertEqual(info.last_startup_info.timestamp, new_timestamp)

  def testWriteClientSnapshotHistoryUpdatesOnlyLastClientTimestamp(self):
    client_id = "C.0000000000000000"
    self._InitializeClient(client_id)

    client_old = objects.ClientSnapshot(client_id=client_id)
    client_old.kernel = "1.0.0"
    client_old.startup_info.client_info.client_name = "foo"
    self.db.WriteClientSnapshot(client_old)

    old_timestamp = self.db.ReadClientSnapshot(client_id).timestamp

    startup_info = rdf_client.StartupInfo()
    startup_info.client_info.client_name = "bar"
    self.db.WriteClientStartupInfo(client_id, startup_info)

    startup_timestamp = self.db.ReadClientStartupInfo(client_id).timestamp

    client_new = objects.ClientSnapshot(client_id=client_id)
    client_new.kernel = "2.0.0"
    client_new.startup_info.client_info.client_name = "baz"
    client_new.timestamp = rdfvalue.RDFDatetime.Lerp(
        0.5, start_time=old_timestamp, end_time=startup_timestamp)
    self.db.WriteClientSnapshotHistory([client_new])

    info = self.db.ReadClientFullInfo(client_id)
    last_snapshot = info.last_snapshot
    last_startup_info = info.last_startup_info
    self.assertEqual(last_snapshot.kernel, "2.0.0")
    self.assertEqual(last_snapshot.startup_info.client_info.client_name, "baz")
    self.assertEqual(last_snapshot.timestamp, client_new.timestamp)
    self.assertEqual(last_startup_info.client_info.client_name, "bar")
    self.assertEqual(last_startup_info.timestamp, startup_timestamp)

  def testWriteClientSnapshotHistoryRaiseTypeError(self):
    client_id = "C.0000000000000000"
    self._InitializeClient(client_id)

    client = objects.ClientMetadata()
    client.os_version = "16.04"
    client.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2010-04-10")

    with self.assertRaisesRegexp(TypeError, "client instance"):
      self.db.WriteClientSnapshotHistory([client])

  def testWriteClientSnapshotHistoryRaiseValueErrorOnEmpty(self):
    with self.assertRaisesRegexp(ValueError, "empty"):
      self.db.WriteClientSnapshotHistory([])

  def testWriteClientSnapshotHistoryRaiseValueErrorOnNonUniformIds(self):
    client_id_a = "C.000000000000000a"
    client_id_b = "C.000000000000000b"
    self._InitializeClient(client_id_a)
    self._InitializeClient(client_id_b)

    client_a = objects.ClientSnapshot(client_id=client_id_a)
    client_a.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2010-05-12")

    client_b = objects.ClientSnapshot(client_id=client_id_b)
    client_b.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2010-06-12")

    with self.assertRaisesRegexp(ValueError, "client id"):
      self.db.WriteClientSnapshotHistory([client_a, client_b])

  def testWriteClientSnapshotHistoryRaiseAttributeError(self):
    client_id = "C.0000000000000000"
    self._InitializeClient(client_id)

    client = objects.ClientSnapshot(client_id=client_id)
    client.kernel = "1.2.3"
    client.startup_info.client_info.client_version = 42

    with self.assertRaisesRegexp(AttributeError, "timestamp"):
      self.db.WriteClientSnapshotHistory([client])

  def testWriteClientSnapshotHistoryRaiseOnNonExistingClient(self):
    client_id = "C.0000000000000000"

    client = objects.ClientSnapshot(client_id=client_id)
    client.kernel = "1.2.3"
    client.timestamp = rdfvalue.RDFDatetime.FromHumanReadable("2001-01-01")

    with self.assertRaises(db.UnknownClientError):
      self.db.WriteClientSnapshotHistory([client])

  def testClientStartupInfo(self):
    """StartupInfo is written to a separate table, make sure the merge works."""
    d = self.db

    client_id = "C.fc413187fefa1dcf"
    self._InitializeClient(client_id)

    client = objects.ClientSnapshot(client_id=client_id, kernel="12.3")
    client.startup_info = rdf_client.StartupInfo(boot_time=123)
    client.knowledge_base.fqdn = "test1234.examples.com"
    d.WriteClientSnapshot(client)

    client = d.ReadClientSnapshot(client_id)
    self.assertEqual(client.startup_info.boot_time, 123)

    client.kernel = "12.4"
    client.startup_info = rdf_client.StartupInfo(boot_time=124)
    d.WriteClientSnapshot(client)

    client.kernel = "12.5"
    client.startup_info = rdf_client.StartupInfo(boot_time=125)
    d.WriteClientSnapshot(client)

    hist = d.ReadClientSnapshotHistory(client_id)
    self.assertEqual(len(hist), 3)
    startup_infos = [cl.startup_info for cl in hist]
    self.assertEqual([si.boot_time for si in startup_infos], [125, 124, 123])

    # StartupInfos written using WriteClient show up in the StartupInfoHistory.
    history = d.ReadClientStartupInfoHistory(client_id)
    self.assertEqual(len(history), 3)
    self.assertEqual(startup_infos, history)

  def testClientSummary(self):
    d = self.db

    client_id_1 = "C.0000000000000001"
    client_id_2 = "C.0000000000000002"
    client_id_3 = "C.0000000000000003"
    self._InitializeClient(client_id_1)
    self._InitializeClient(client_id_2)
    self._InitializeClient(client_id_3)

    d.WriteClientSnapshot(
        objects.ClientSnapshot(
            client_id=client_id_1,
            knowledge_base=rdf_client.KnowledgeBase(
                fqdn="test1234.examples.com"),
            kernel="12.3"))
    d.WriteClientSnapshot(
        objects.ClientSnapshot(
            client_id=client_id_1,
            knowledge_base=rdf_client.KnowledgeBase(
                fqdn="test1234.examples.com"),
            kernel="12.4"))

    d.WriteClientSnapshot(
        objects.ClientSnapshot(
            client_id=client_id_2,
            knowledge_base=rdf_client.KnowledgeBase(
                fqdn="test1235.examples.com"),
            kernel="12.4"))

    hist = d.ReadClientSnapshotHistory(client_id_1)
    self.assertEqual(len(hist), 2)

    # client_3 should be excluded - no snapshot yet
    res = d.MultiReadClientSnapshot([client_id_1, client_id_2, client_id_3])
    self.assertEqual(len(res), 3)
    self.assertIsInstance(res[client_id_1], objects.ClientSnapshot)
    self.assertIsInstance(res[client_id_2], objects.ClientSnapshot)
    self.assertIsInstance(res[client_id_1].timestamp, rdfvalue.RDFDatetime)
    self.assertIsNotNone(res[client_id_2].timestamp)
    self.assertEqual(res[client_id_1].knowledge_base.fqdn,
                     "test1234.examples.com")
    self.assertEqual(res[client_id_1].kernel, "12.4")
    self.assertEqual(res[client_id_2].knowledge_base.fqdn,
                     "test1235.examples.com")
    self.assertFalse(res[client_id_3])

  def testClientValidates(self):
    d = self.db

    # Write some metadata so the client write would otherwise succeed.
    client_id = "C.fc413187fefa1dcf"
    d.WriteClientMetadata(client_id, fleetspeak_enabled=True)
    with self.assertRaises(TypeError):
      d.WriteClientSnapshot("test1235.examples.com")

  def testClientKeywords(self):
    d = self.db
    client_id_1 = "C.0000000000000001"
    client_id_2 = "C.0000000000000002"
    client_id_3 = "C.0000000000000003"
    for cid in [client_id_1, client_id_2, client_id_3]:
      d.WriteClientMetadata(cid, fleetspeak_enabled=True)

    # Typical keywords are usernames and prefixes of hostnames.
    d.AddClientKeywords(client_id_1, [
        "joe", "machine.test.example1.com", "machine.test.example1",
        "machine.test", "machine", u"⊙_ʘ"
    ])
    d.AddClientKeywords(client_id_2, [
        "fred", "machine.test.example2.com", "machine.test.example2",
        "machine.test", "machine", u"ಠ_ಠ"
    ])
    res = d.ListClientsForKeywords(["fred", "machine", "missing"])
    self.assertEqual(res["fred"], [client_id_2])
    self.assertEqual(sorted(res["machine"]), [client_id_1, client_id_2])
    self.assertEqual(res["missing"], [])

    for kw, client_id in [(u"⊙_ʘ", client_id_1), (u"ಠ_ಠ", client_id_2),
                          (utils.SmartStr(u"⊙_ʘ"), client_id_1)]:
      res = d.ListClientsForKeywords([kw])
      self.assertEqual(
          res[kw], [client_id], "Expected [%s] when reading keyword %s, got %s"
          % (client_id, kw, res[kw]))

  def testClientKeywordsTimeRanges(self):
    d = self.db
    client_id = "C.0000000000000001"
    self._InitializeClient(client_id)

    d.AddClientKeywords(client_id, ["hostname1"])
    change_time = rdfvalue.RDFDatetime.Now()
    d.AddClientKeywords(client_id, ["hostname2"])

    res = d.ListClientsForKeywords(
        ["hostname1", "hostname2"], start_time=change_time)
    self.assertEqual(res["hostname1"], [])
    self.assertEqual(res["hostname2"], [client_id])

  def testRemoveClientKeyword(self):
    d = self.db
    client_id = "C.0000000000000001"
    temporary_kw = "investigation42"
    self._InitializeClient(client_id)
    d.AddClientKeywords(client_id, [
        "joe", "machine.test.example.com", "machine.test.example",
        "machine.test", temporary_kw
    ])
    self.assertEqual(
        d.ListClientsForKeywords([temporary_kw])[temporary_kw], [client_id])
    d.RemoveClientKeyword(client_id, temporary_kw)
    self.assertEqual(d.ListClientsForKeywords([temporary_kw])[temporary_kw], [])
    self.assertEqual(d.ListClientsForKeywords(["joe"])["joe"], [client_id])

  def testClientLabels(self):
    d = self.db
    client_id = "C.0000000000000001"
    self._InitializeClient(client_id)

    self.assertEqual(d.ReadClientLabels(client_id), [])

    d.AddClientLabels(client_id, "owner1", ["label1"])
    d.AddClientLabels(client_id, "owner2", ["label2", "label3"])

    all_labels = [
        objects.ClientLabel(name="label1", owner="owner1"),
        objects.ClientLabel(name="label2", owner="owner2"),
        objects.ClientLabel(name="label3", owner="owner2")
    ]

    self.assertEqual(d.ReadClientLabels(client_id), all_labels)
    self.assertEqual(d.ReadClientLabels("C.0000000000000002"), [])

    # Can't hurt to insert this one again.
    d.AddClientLabels(client_id, "owner1", ["label1"])
    self.assertEqual(d.ReadClientLabels(client_id), all_labels)

    d.RemoveClientLabels(client_id, "owner1", ["does not exist"])
    self.assertEqual(d.ReadClientLabels(client_id), all_labels)

    # Label3 is actually owned by owner2.
    d.RemoveClientLabels(client_id, "owner1", ["label3"])
    self.assertEqual(d.ReadClientLabels(client_id), all_labels)

    d.RemoveClientLabels(client_id, "owner2", ["label3"])
    self.assertEqual(
        d.ReadClientLabels(client_id), [
            objects.ClientLabel(name="label1", owner="owner1"),
            objects.ClientLabel(name="label2", owner="owner2"),
        ])

  def testClientLabelsUnicode(self):
    d = self.db
    client_id = "C.0000000000000001"
    self._InitializeClient(client_id)

    self.assertEqual(d.ReadClientLabels(client_id), [])

    d.AddClientLabels(client_id, "owner1", [u"⛄࿄1"])
    d.AddClientLabels(client_id, "owner2", [u"⛄࿄2"])
    d.AddClientLabels(client_id, "owner2", [utils.SmartStr(u"⛄࿄3")])

    all_labels = [
        objects.ClientLabel(name=u"⛄࿄1", owner="owner1"),
        objects.ClientLabel(name=u"⛄࿄2", owner="owner2"),
        objects.ClientLabel(name=u"⛄࿄3", owner="owner2")
    ]

    self.assertEqual(d.ReadClientLabels(client_id), all_labels)

    d.RemoveClientLabels(client_id, "owner1", ["does not exist"])
    self.assertEqual(d.ReadClientLabels(client_id), all_labels)

    # This label is actually owned by owner2.
    d.RemoveClientLabels(client_id, "owner1", [u"⛄࿄3"])
    self.assertEqual(d.ReadClientLabels(client_id), all_labels)

    d.RemoveClientLabels(client_id, "owner2", [u"⛄࿄3"])
    self.assertEqual(
        d.ReadClientLabels(client_id), [
            objects.ClientLabel(name=u"⛄࿄1", owner="owner1"),
            objects.ClientLabel(name=u"⛄࿄2", owner="owner2")
        ])

  def testReadAllLabelsReturnsLabelsFromSingleClient(self):
    d = self.db

    client_id = "C.0000000000000001"
    self._InitializeClient(client_id)

    d.AddClientLabels(client_id, "owner1", [u"foo"])

    all_labels = d.ReadAllClientLabels()
    self.assertEqual(all_labels,
                     [objects.ClientLabel(name="foo", owner="owner1")])

  def testReadAllLabelsReturnsLabelsFromMultipleClients(self):
    d = self.db

    client_id_1 = "C.0000000000000001"
    self._InitializeClient(client_id_1)
    client_id_2 = "C.0000000000000002"
    self._InitializeClient(client_id_2)

    d.AddClientLabels(client_id_1, "owner1", [u"foo"])
    d.AddClientLabels(client_id_2, "owner1", [u"foo"])
    d.AddClientLabels(client_id_1, "owner2", [u"bar"])
    d.AddClientLabels(client_id_2, "owner2", [u"bar"])

    all_labels = sorted(d.ReadAllClientLabels(), key=lambda l: l.name)
    self.assertEqual(all_labels, [
        objects.ClientLabel(name="bar", owner="owner2"),
        objects.ClientLabel(name="foo", owner="owner1")
    ])

  def testReadClientStartupInfoHistory(self):
    d = self.db

    client_id = "C.0000000050000001"
    si = rdf_client.StartupInfo(boot_time=1)

    with self.assertRaises(db.UnknownClientError):
      d.WriteClientStartupInfo(client_id, si)

    self._InitializeClient(client_id)

    d.WriteClientStartupInfo(client_id, si)
    si.boot_time = 2
    d.WriteClientStartupInfo(client_id, si)
    si.boot_time = 3
    d.WriteClientStartupInfo(client_id, si)

    last_is = d.ReadClientStartupInfo(client_id)
    self.assertIsInstance(last_is, rdf_client.StartupInfo)
    self.assertEqual(last_is.boot_time, 3)
    self.assertIsInstance(last_is.timestamp, rdfvalue.RDFDatetime)

    hist = d.ReadClientStartupInfoHistory(client_id)
    self.assertEqual(len(hist), 3)
    self.assertEqual([si.boot_time for si in hist], [3, 2, 1])
    self.assertIsInstance(hist[0].timestamp, rdfvalue.RDFDatetime)
    self.assertGreater(hist[0].timestamp, hist[1].timestamp)
    self.assertGreater(hist[1].timestamp, hist[2].timestamp)

    md = self.db.ReadClientMetadata(client_id)
    self.assertEqual(md.startup_info_timestamp, hist[0].timestamp)

    self.assertIsNone(d.ReadClientStartupInfo("C.0000000000000000"))
    self.assertEqual(d.ReadClientStartupInfoHistory("C.0000000000000000"), [])

  def _SetUpReadClientStartupInfoHistoryTest(self):
    d = self.db

    self.client_id = "C.0000000050000001"
    self._InitializeClient(self.client_id)

    timestamps = [rdfvalue.RDFDatetime.Now()]

    si = rdf_client.StartupInfo(boot_time=1)
    d.WriteClientStartupInfo(self.client_id, si)
    timestamps.append(d.ReadClientStartupInfo(self.client_id).timestamp)

    timestamps.append(rdfvalue.RDFDatetime.Now())

    si = rdf_client.StartupInfo(boot_time=2)
    d.WriteClientStartupInfo(self.client_id, si)
    timestamps.append(d.ReadClientStartupInfo(self.client_id).timestamp)

    timestamps.append(rdfvalue.RDFDatetime.Now())

    return timestamps

  def testReadClientStartupInfoHistoryWithEmptyTimerange(self):
    d = self.db

    self._SetUpReadClientStartupInfoHistoryTest()

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(None, None))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].boot_time, 2)
    self.assertEqual(hist[1].boot_time, 1)

  def testReadClientStartupInfoHistoryWithTimerangeWithBothFromTo(self):
    d = self.db

    ts = self._SetUpReadClientStartupInfoHistoryTest()

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[0], ts[2]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].boot_time, 1)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[2], ts[4]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].boot_time, 2)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[0], ts[4]))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].boot_time, 2)
    self.assertEqual(hist[1].boot_time, 1)

  def testReadClientStartupInfoHistoryWithTimerangeWithFromOnly(self):
    d = self.db

    ts = self._SetUpReadClientStartupInfoHistoryTest()

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[0], None))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].boot_time, 2)
    self.assertEqual(hist[1].boot_time, 1)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[2], None))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].boot_time, 2)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[4], None))
    self.assertEqual(len(hist), 0)

  def testReadClientStartupInfoHistoryWithTimerangeWithToOnly(self):
    d = self.db

    ts = self._SetUpReadClientStartupInfoHistoryTest()

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(None, ts[0]))
    self.assertEqual(len(hist), 0)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(None, ts[2]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].boot_time, 1)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(None, ts[4]))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].boot_time, 2)
    self.assertEqual(hist[1].boot_time, 1)

  def testReadClientStartupInfoHistoryWithTimerangeEdgeCases(self):
    # Timerange should work as [from, to]. I.e. "from" is inclusive and "to"
    # is inclusive.

    d = self.db

    ts = self._SetUpReadClientStartupInfoHistoryTest()

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[1], ts[1]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].boot_time, 1)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[1], ts[2]))
    self.assertEqual(len(hist), 1)
    self.assertEqual(hist[0].boot_time, 1)

    hist = d.ReadClientStartupInfoHistory(
        self.client_id, timerange=(ts[1], ts[3]))
    self.assertEqual(len(hist), 2)
    self.assertEqual(hist[0].boot_time, 2)
    self.assertEqual(hist[1].boot_time, 1)

  def testCrashHistory(self):
    d = self.db

    client_id = "C.0000000050000001"
    ci = rdf_client.ClientCrash(timestamp=12345, crash_message="Crash #1")

    with self.assertRaises(db.UnknownClientError):
      d.WriteClientCrashInfo(client_id, ci)

    self._InitializeClient(client_id)

    d.WriteClientCrashInfo(client_id, ci)
    ci.crash_message = "Crash #2"
    d.WriteClientCrashInfo(client_id, ci)
    ci.crash_message = "Crash #3"
    d.WriteClientCrashInfo(client_id, ci)

    last_is = d.ReadClientCrashInfo(client_id)
    self.assertIsInstance(last_is, rdf_client.ClientCrash)
    self.assertEqual(last_is.crash_message, "Crash #3")
    self.assertIsInstance(last_is.timestamp, rdfvalue.RDFDatetime)

    hist = d.ReadClientCrashInfoHistory(client_id)
    self.assertEqual(len(hist), 3)
    self.assertEqual([ci.crash_message for ci in hist],
                     ["Crash #3", "Crash #2", "Crash #1"])
    self.assertIsInstance(hist[0].timestamp, rdfvalue.RDFDatetime)
    self.assertGreater(hist[0].timestamp, hist[1].timestamp)
    self.assertGreater(hist[1].timestamp, hist[2].timestamp)

    md = self.db.ReadClientMetadata(client_id)
    self.assertEqual(md.last_crash_timestamp, hist[0].timestamp)

    self.assertIsNone(d.ReadClientCrashInfo("C.0000000000000000"))
    self.assertEqual(d.ReadClientCrashInfoHistory("C.0000000000000000"), [])

  def testEmptyCrashHistory(self):
    client_id = "C.0000000050000001"
    self.assertIsNone(self.db.ReadClientCrashInfo(client_id))
    self.assertEqual(self.db.ReadClientCrashInfoHistory(client_id), [])

  def testReadClientFullInfoPartialReads(self):
    client_id = "C.0000000050000001"
    self._InitializeClient(client_id)
    self.assertIsNotNone(self.db.ReadClientFullInfo(client_id))

  def testReadClientFullInfoReturnsCorrectResult(self):
    d = self.db

    client_id = "C.0000000050000001"
    self._InitializeClient(client_id)

    cl = objects.ClientSnapshot(
        client_id=client_id,
        knowledge_base=rdf_client.KnowledgeBase(fqdn="test1234.examples.com"),
        kernel="12.3")
    d.WriteClientSnapshot(cl)
    d.WriteClientMetadata(client_id, certificate=CERT)
    si = rdf_client.StartupInfo(boot_time=1)
    d.WriteClientStartupInfo(client_id, si)
    d.AddClientLabels(client_id, "test_owner", ["test_label"])

    full_info = d.ReadClientFullInfo(client_id)
    self.assertEqual(full_info.last_snapshot, cl)
    self.assertEqual(full_info.metadata.certificate, CERT)
    self.assertEqual(full_info.last_startup_info, si)
    self.assertEqual(
        full_info.labels,
        [objects.ClientLabel(owner="test_owner", name="test_label")])

  def _SetupFullInfoClients(self):
    for i in range(10):
      client_id = "C.000000005000000%d" % i
      self._InitializeClient(client_id)

      cl = objects.ClientSnapshot(
          client_id=client_id,
          knowledge_base=rdf_client.KnowledgeBase(fqdn="test%d.examples.com" %
                                                  i),
          kernel="12.3.%d" % i)
      self.db.WriteClientSnapshot(cl)
      self.db.WriteClientMetadata(client_id, certificate=CERT)
      si = rdf_client.StartupInfo(boot_time=i)
      self.db.WriteClientStartupInfo(client_id, si)
      self.db.AddClientLabels(
          client_id, "test_owner",
          ["test_label-a-%d" % i, "test_label-b-%d" % i])

  def _VerifySnapshots(self, snapshots):
    snapshots = sorted(snapshots, key=lambda s: s.client_id)
    self.assertEqual(len(snapshots), 10)
    for i, s in enumerate(snapshots):
      self.assertEqual(s.client_id, "C.000000005000000%d" % i)
      self.assertEqual(s.knowledge_base.fqdn, "test%d.examples.com" % i)

  def _VerifyFullInfos(self, c_infos):
    c_infos = sorted(c_infos, key=lambda c: c.last_snapshot.client_id)
    for i, full_info in enumerate(c_infos):
      self.assertEqual(full_info.last_snapshot.client_id,
                       "C.000000005000000%d" % i)
      self.assertEqual(full_info.metadata.certificate, CERT)
      self.assertEqual(full_info.last_startup_info.boot_time, i)
      self.assertEqual(
          sorted(full_info.labels, key=lambda l: l.name), [
              objects.ClientLabel(
                  owner="test_owner", name="test_label-a-%d" % i),
              objects.ClientLabel(
                  owner="test_owner", name="test_label-b-%d" % i)
          ])

  def testIterateAllClientsFullInfo(self):
    self._SetupFullInfoClients()
    self._VerifyFullInfos(self.db.IterateAllClientsFullInfo())

  def testIterateAllClientsFullInfoSmallBatches(self):
    self._SetupFullInfoClients()
    self._VerifyFullInfos(self.db.IterateAllClientsFullInfo(batch_size=2))

  def testIterateAllClientSnapshots(self):
    self._SetupFullInfoClients()
    snapshots = self.db.IterateAllClientSnapshots()
    self._VerifySnapshots(snapshots)

  def testIterateAllClientSnapshotsSmallBatches(self):
    self._SetupFullInfoClients()
    snapshots = self.db.IterateAllClientSnapshots(batch_size=2)
    self._VerifySnapshots(snapshots)

  def _SetupLastPingClients(self, now):
    time_past = now - rdfvalue.Duration("1d")

    client_ids_to_ping = {}
    for i in range(10):
      client_id = "C.000000005000000%d" % i
      self._InitializeClient(client_id)

      self.db.WriteClientSnapshot(objects.ClientSnapshot(client_id=client_id))
      ping = (time_past if i % 2 == 0 else now)
      self.db.WriteClientMetadata(client_id, last_ping=ping)

      client_ids_to_ping[client_id] = ping

    return client_ids_to_ping

  def testMultiReadClientsFullInfoFiltersClientsByLastPingTime(self):
    d = self.db

    base_time = rdfvalue.RDFDatetime.Now()
    cutoff_time = base_time - rdfvalue.Duration("1s")
    client_ids_to_ping = self._SetupLastPingClients(base_time)

    expected_client_ids = [
        cid for cid, ping in client_ids_to_ping.items() if ping == base_time
    ]
    full_infos = d.MultiReadClientFullInfo(
        client_ids_to_ping, min_last_ping=cutoff_time)
    self.assertItemsEqual(expected_client_ids, full_infos)
