import pytest
from unittest import mock

from .doubles import (
    MockAccount,
)
from yosai import (
    AccountStoreRealm,
    IncorrectCredentialsException,
    settings,
)

from yosai.authc import (
    AllRealmsSuccessfulStrategy,
    AtLeastOneRealmSuccessfulStrategy,
    AuthenticationSettings,
    CryptContextFactory,
    DefaultAuthcService,
    DefaultAuthenticationAttempt,
    DefaultHashService,
    DefaultPasswordService,
    FirstRealmSuccessfulStrategy,
    IAuthenticationToken,
    UsernamePasswordToken,
)

from passlib.context import CryptContext


@pytest.fixture(scope="function")
def all_realms_successful_strategy():
    return AllRealmsSuccessfulStrategy()


@pytest.fixture(scope="function")
def alo_realms_successful_strategy():
    return AtLeastOneRealmSuccessfulStrategy()


@pytest.fixture(scope="function")
def first_realm_successful_strategy():
    return FirstRealmSuccessfulStrategy()


@pytest.fixture(scope="function")
def authc_config():
    return {
        "hash_algorithms": {
            "bcrypt_sha256": {
                "default_rounds": 200000,
            },
            "sha256_crypt": {
                "default_rounds": 110000,
                "max_rounds": 1000000,
                "min_rounds": 1000,
                "salt_size": 16}},
        "private_salt": "privatesalt"
    }


@pytest.fixture(scope='function')
def username_password_token():
    return UsernamePasswordToken(username='user', 
                                 password='secret',
                                 remember_me=False, 
                                 host='127.0.0.1') 


@pytest.fixture(scope='function')
def mock_token():
    class MockToken(IAuthenticationToken, object):
        @property
        def principal(self):
            pass

        @property
        def credentials(self):
            pass

    return MockToken()


@pytest.fixture(scope='function')
def patched_authc_settings(authc_config, monkeypatch):
    monkeypatch.setattr(settings, 'AUTHC_CONFIG', authc_config)
    return AuthenticationSettings()

@pytest.fixture(scope='function')
def default_authc_service():
    return DefaultAuthcService()

@pytest.fixture(scope='function')
def first_accountstorerealm_succeeds(monkeypatch):
    def mock_return(self, token):
        return MockAccount(account_id=12345)
    monkeypatch.setattr(AccountStoreRealm, 'authenticate_account', mock_return)
    return AccountStoreRealm() 

@pytest.fixture(scope='function')
def first_accountstorerealm_fails(monkeypatch):
    def mock_return(self, token):
        raise IncorrectCredentialsException
    monkeypatch.setattr(AccountStoreRealm, 'authenticate_account', mock_return)
    return AccountStoreRealm() 

@pytest.fixture(scope='function')
def second_accountstorerealm_fails(monkeypatch):
    def mock_return(self, token):
        raise IncorrectCredentialsException
    monkeypatch.setattr(AccountStoreRealm, 'authenticate_account', mock_return)
    return AccountStoreRealm() 

@pytest.fixture(scope='function')
def second_accountstorerealm_succeeds(monkeypatch):
    def mock_return(self, token):
        return MockAccount(account_id=67890)
    monkeypatch.setattr(AccountStoreRealm, 'authenticate_account', mock_return) 
    return AccountStoreRealm() 

@pytest.fixture(scope='function')
def one_accountstorerealm_succeeds(first_accountstorerealm_succeeds):
    return {first_accountstorerealm_succeeds}

@pytest.fixture(scope='function')
def one_accountstorerealm_fails(first_accountstorerealm_fails):
    return {first_accountstorerealm_fails}

@pytest.fixture(scope='function')
def two_accountstorerealms_fails(first_accountstorerealm_fails):
    return {first_accountstorerealm_fails, first_accountstorerealm_fails}

@pytest.fixture(scope='function')
def two_accountstorerealms_succeeds(first_accountstorerealm_succeeds,
                                    second_accountstorerealm_succeeds):
    return {first_accountstorerealm_succeeds, second_accountstorerealm_succeeds}

@pytest.fixture(scope='function')
def two_accountstorerealms_fails(first_accountstorerealm_fails,
                                 second_accountstorerealm_fails):
    return {first_accountstorerealm_fails, second_accountstorerealm_fails}

@pytest.fixture(scope='function')
def default_authc_attempt(username_password_token, one_accountstorerealm_succeeds): 
    return DefaultAuthenticationAttempt(username_password_token, 
                                        one_accountstorerealm_succeeds) 

@pytest.fixture(scope='function')
def fail_authc_attempt(username_password_token, one_accountstorerealm_fails): 
    return DefaultAuthenticationAttempt(username_password_token, 
                                        one_accountstorerealm_fails) 

@pytest.fixture(scope='function')
def fail_multi_authc_attempt(username_password_token, two_accountstorerealms_fails): 
    return DefaultAuthenticationAttempt(username_password_token, 
                                        two_accountstorerealms_fails) 

@pytest.fixture(scope='function')
def realmless_authc_attempt(username_password_token):
    return DefaultAuthenticationAttempt(username_password_token, set()) 

@pytest.fixture(scope='function')
def mock_token_attempt(mock_token, one_accountstorerealm_succeeds): 
    return DefaultAuthenticationAttempt(mock_token, one_accountstorerealm_succeeds)

@pytest.fixture(scope='function')
def multirealm_authc_attempt(username_password_token, two_accountstorerealms_succeeds): 
    return DefaultAuthenticationAttempt(username_password_token, 
                                        two_accountstorerealms_succeeds)

@pytest.fixture(scope='function')
def cryptcontext_factory():
    authc_settings = AuthenticationSettings()
    return CryptContextFactory(authc_settings)


@pytest.fixture(scope='function')
def crypt_context():
    return CryptContext(schemes=['sha256_crypt'])


@pytest.fixture(scope='function')
def default_context():
    return {'schemes': ['sha256_crypt'],
            'sha256_crypt__default_rounds': 180000}


@pytest.fixture(scope='function')
def default_encrypted_password():
    # bcrypt hash of 'privatesaltwithcleartext':
    return '$bcrypt-sha256$2a,12$HXuLhfmy1I1cWb46CC4KtO$hGXldB0fsNTwp6sRQJToAQDeUjPMW36' 


@pytest.fixture(scope='function')
def default_hash_service():
    return DefaultHashService()


@pytest.fixture(scope='function')
def default_password_service():
    return DefaultPasswordService()


@pytest.fixture(scope='function')
def private_salt():
    return 'privatesaltysnack'
