#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/sm7435-common',
    'hardware/motorola',
    'hardware/qcom-caf/common/libqti-perfd-client',
    'hardware/qcom-caf/sm8450',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/dataservices',
]


libs_add_vendor_suffix = (
    'vendor.qti.hardware.qccsyshal@1.0',
    'vendor.qti.hardware.qccsyshal@1.1',
    'vendor.qti.imsrtpservice@3.0',
    'vendor.qti.diaghal@1.0',
    'vendor.qti.hardware.wifidisplaysession@1.0',
    'com.qualcomm.qti.dpm.api@1.0',
)


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    if partition != 'vendor':
        return None

    return f'{lib}_{partition}'


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    libs_add_vendor_suffix: lib_fixup_vendor_suffix,
}


blob_fixups: blob_fixups_user_type = {
    'system_ext/etc/permissions/moto-telephony.xml': blob_fixup().regex_replace(
        '/system/', '/system_ext/'
    ),
    'system_ext/lib64/libwfdnative.so': blob_fixup().add_needed(
        'libinput_shim.so'
    ),
    'system_ext/lib64/vendor.qti.hardware.qccsyshal@1.2-halimpl.so': blob_fixup().replace_needed(
        'libprotobuf-cpp-full.so', 'libprotobuf-cpp-full-21.7.so'
    ),
    (
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/lib64/libqtikeymint.so',
    ): blob_fixup()
    .replace_needed(
        'android.hardware.security.keymint-V1-ndk_platform.so',
        'android.hardware.security.keymint-V1-ndk.so',
    )
    .replace_needed(
        'android.hardware.security.secureclock-V1-ndk_platform.so',
        'android.hardware.security.secureclock-V1-ndk.so',
    )
    .replace_needed(
        'android.hardware.security.sharedsecret-V1-ndk_platform.so',
        'android.hardware.security.sharedsecret-V1-ndk.so',
    )
    .add_needed('android.hardware.security.rkp-V1-ndk.so'),
    'vendor/bin/init.kernel.post_boot.sh': blob_fixup().regex_replace(
        'ro.boot.using_zram_from_fstab', 'ro.vendor.zram.swapon'
    ),
    'vendor/etc/sensors/hals.conf': blob_fixup().add_line_if_missing(
        'sensors.moto_ext.so',
    ),
    'vendor/etc/public.libraries.txt': blob_fixup().regex_replace(
        'libqti-perfd-client.so\n', ''
    ),
    'vendor/lib64/libmotext_inf.so': blob_fixup().remove_needed('libril.so'),
    'system_ext/priv-app/ims/ims.apk': blob_fixup().apktool_patch(
        'ims-patches'
    ),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup().add_needed(
        'libhidlbase_shim.so'
    ),
    'vendor/lib64/libqcodec2_core.so': blob_fixup().add_needed(
        'libcodec2_shim.so'
    ),
    'vendor/lib64/sensors.moto.so': blob_fixup().add_needed('libbase_shim.so'),
    (
        'vendor/etc/media_codecs_parrot_v0.xml',
        'vendor/etc/media_codecs_parrot_v1.xml',
        'vendor/etc/media_codecs_parrot_v2.xml',
        'vendor/etc/media_codecs_ravelin.xml',
    ): blob_fixup().regex_replace(
        '.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio|dolby_audio).*\n',
        '',
    ),
    (
        'vendor/lib64/libdpps.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
    ): blob_fixup().replace_needed(
        'libtinyxml2.so', 'libtinyxml2-v34.so'
    ),
}

module = ExtractUtilsModule(
    'sm7435-common',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)
