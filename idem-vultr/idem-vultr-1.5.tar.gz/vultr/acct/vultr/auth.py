async def gather(hub):
    """
    Turn a profile location into a DCID
    Turn a profile ssh_key_name into an SSHKEYID
    """
    sub_profiles = {}

    for profile, ctx in hub.acct.PROFILES.get("vultr", {}).items():
        # Verify that management howt and api_version are part of the context
        management_host = ctx.pop("management_host", "api.vultr.com")
        api_version = ctx.pop("api_version", "v1")
        ctx["api_url"] = f"https://{management_host}/{api_version}"

        # Context for making vultr calls from this plugin
        temp_ctx = {"acct": ctx, "test": False}

        # add a DCID based on the location in the profile to the ctx
        location = ctx.pop("location", None)
        if location:
            region = hub.exec.vultr.util.get(
                location,
                await hub.exec.vultr.regions.list(temp_ctx),
                ["DCID", "regioncode", "name"],
            )
            if "DCID" not in region:
                raise ValueError(f"Location not available: {location}")
            ctx["DCID"] = region["DCID"]

        # add an SSHKEYID based on the ssh_key information in the profile to the ctx
        key_name = ctx.pop("ssh_key_name", None)
        if key_name:
            key_file = ctx.pop("ssh_key_file", None)
            # This will fail if the key doesn't exist and the file is not provided
            result = await hub.states.vultr.ssh_key.present(
                temp_ctx, name=key_name, ssh_key=key_file
            )
            assert result["result"] is True, result["comment"]
            hub.log.debug(result["comment"])

            ctx["SSHKEYID"] = hub.exec.vultr.util.get(
                key_name,
                await hub.exec.vultr.ssh_key.list(temp_ctx),
                ["SSHKEYID", "ssh_key", "name"],
            )["SSHKEYID"]

            if key_file:
                # Make sure the key is up to date
                status, ret = await hub.exec.vultr.ssh_key.update(
                    temp_ctx,
                    key_id=ctx["SSHKEYID"],
                    name=key_name,
                    ssh_key=ctx.pop("ssh_key_file", None),
                )
                assert status, ret

        sub_profiles[profile] = ctx

    return sub_profiles
