var Verifier = artifacts.require("./Verifier.sol");
var Miximus = artifacts.require("./roll_up.sol");

// File generated from running build process of `roll_up`
var vk = require("./vk.json");

module.exports = function(deployer) {
    deployer.deploy(
        Verifier,
        vk.a1,
        vk.a2,
        vk.b,
        vk.c1,
        vk.c2,
        vk.g1,
        vk.g2,
        vk.gb1,
        vk.gb2_1,
        vk.gb2_2,
        vk.z1,
        vk.z2,
    ).then(async () => {
        const verifier = await Verifier.deployed();
        await deployer.deploy(
            Miximus,
            verifier.address,
            // FIXME: Use real root
            "0x1eaa408e63a9f398689c6dd1bff4607276c66172a0f7c9fa916473278158ecbe"
        );
    });
};
