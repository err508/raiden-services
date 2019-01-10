import gevent


def test_bp_dispatch(monitoring_service, generate_raiden_client, wait_for_blocks):
    """Test if server accepts an incoming balance proof message"""
    c1, c2 = generate_raiden_client(), generate_raiden_client()
    channel_id = c1.open_channel(c2.address)
    wait_for_blocks(1)  # wait for ChannelOpened event to be confirmed
    gevent.sleep(0.1)   # ...and processed
    bp = c2.get_balance_proof(c1.address, transferred_amount=1, nonce=1)
    monitor_request = c1.get_monitor_request(c2.address, bp, 1, monitoring_service.address)
    transport = monitoring_service.transport

    transport.receive_fake_data(monitor_request.serialize_full())
    monitoring_service.wait_tasks()
    assert (channel_id, c1.address) in monitoring_service.monitor_requests
