package main

import (

	//"golang.org/x/crypto/nacl/secretbox"
	//"crypto/rand"
	//"io"
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"log"
	"math/big"

	"golang.org/x/crypto/scrypt"

	"github.com/aws/aws-lambda-go/lambda"
)

//GenerateScryptKey Generate scypt kets on the basis of saltByes and PassphraseBytes
func GenerateScryptKey(saltBytes []byte, passphraseBytes []byte) ([]byte, error) {
	//entropy, _ := bip39.NewEntropy(256)
	dk, err := scrypt.Key(passphraseBytes, saltBytes, 32768, 8, 1, 32)
	return dk, err

}

//GenerateRandomString Given length, generates  random string og length length
func GenerateRandomString(length int) string {
	result := ""
	for {
		if len(result) >= length {
			return base64.StdEncoding.EncodeToString([]byte(result))
		}
		num, err := rand.Int(rand.Reader, big.NewInt(int64(127)))
		if err != nil {
			panic(err)
		}
		n := num.Int64()
		// Make sure that the number/byte/letter is inside
		// the range of printable ASCII characters (excluding space and DEL)
		if n > 32 && n < 127 {
			result += string(n)
		}
	}
}

//GenerateRandomSalt given numberOfBytes , generates a randomsaltBytes
func GenerateRandomSalt(numberOfBytes int) []byte {
	nBig, err := rand.Int(rand.Reader, big.NewInt(27))
	if err != nil {
		panic(err)
	}
	n := nBig.Int64()
	log.Printf("Here is a random %T in [0,27) : %d\n", n, n)
	salt := make([]byte, numberOfBytes)
	_, err = rand.Read(salt)
	// Note that err == nil only if we read len(b) bytes.
	if err != nil {
		panic(err)
	}

	return salt
}

//Entropier Generates random bytes whole length will be numberOfBytes
type Entropier interface {
	//The generate netropy function will take an int, for which
	// number of bytes entropy bytes will be generated
	GenerateEntropy(numberOfBytes int) ([]byte, error)
}

//Mnemonicer Generate Mnemonic from the entropy bytes
type Mnemonicer interface {
	GenerateMnemonic(entropy []byte) (string, error)
}

//Passphraser Generate passphrase from the saltBytes and the passphrasebytres
type Passphraser interface {
	GeneratePassphrase(saltBytes int, passphraseBytes int) ([]byte, error)
}

//Seeder Generate seed from the mnemonic and the passphrase
type Seeder interface {
	GenerateSeed(mnemonic string, passphrase []byte) []byte
}

//RootKeyGenerator Generate root keys from the seed
type RootKeyGenerator interface {
	GenerateRootKeys(seed []byte) (*bip32.Key, *bip32.Key)
}

//ChildPublicKeyGenerator Generate child public ket at the index childNumber
type ChildPublicKeyGenerator interface {
	GeneratePublicChildKey(rootPrivateKey *bip32.Key, childNumber uint32) (*bip32.Key, error)
}

//ChildPrivateKeyGenerator Generate child private key at the index childNumber
type ChildPrivateKeyGenerator interface {
	GeneratePrivateChildKey(rootPulicKey *bip32.Key, childNumber uint32) (*bip32.Key, *bip32.Key, error)
}

//HexKeyEncoder hex encoding of the extended key
type HexKeyEncoder interface {
	HexKeyEncoding(extendedKey *bip32.Key) string
}

//BipKeyer Interface for Mnemonic
type BipKeyer interface {
	Entropier
	Mnemonicer
	//Passphraser
	RootKeyGenerator
	ChildPublicKeyGenerator
	ChildPrivateKeyGenerator
	HexKeyEncoder
}

//BipKeys struct for Menmonic
type BipKeys struct {
	Entropy                []byte
	Mnemonic               string
	Passphrase             []byte
	Seed                   []byte
	MnemonicShares         []string
	RootPublicExtendedKey  *bip32.Key
	RootPrivateExtendedKey *bip32.Key
	RootPrivateHexKey      string
}

//GenerateEntropy fulfills the Entropier interface by implementing GenerateEntropy function,
//Will return entropy bytes whose length is equal to numberOfbytes
func (instance *BipKeys) GenerateEntropy(numberOfBytes int) ([]byte, error) {
	entropy, err := bip39.NewEntropy(numberOfBytes)
	if err != nil {
		log.Printf("There is some error generating entropy %s", err)
	}
	return entropy, err
}

//GenerateMnemonic Generates a New Mnemonic from the Entropy bytes
func (instance *BipKeys) GenerateMnemonic(entropy []byte) (string, error) {
	mnemonic, err := bip39.NewMnemonic(entropy)
	if err != nil {
		log.Printf("Some error in generating Mnemonic %s", err)

	}
	return mnemonic, err
}

//GeneratePassphrase generates a passphrase by taking number of bytes for saltBytes and number of bytes for passphraseBytes
func (instance *BipKeys) GeneratePassphrase(saltBytes int, passphraseBytes int) ([]byte, error) {
	salt := GenerateRandomSalt(8)
	passphrase := GenerateRandomString(8)

	password, err := GenerateScryptKey(salt, []byte(passphrase))
	return password, err
}

//GenerateSeed Given a mnemonic and passphrase, will create a seed, its an deterministic operation
func (instance *BipKeys) GenerateSeed(mnemonic string, passphrase []byte) []byte {
	seed := bip39.NewSeed(mnemonic, string(passphrase))
	return seed
}

//RootKeyGenerator Given seed bytes, generates the rootPrivate key and public keym deterministically
func (instance *BipKeys) RootKeyGenerator(seed []byte) (*bip32.Key, *bip32.Key) {
	rootPrivateKey, err := bip32.NewMasterKey(seed)
	if err != nil {
		log.Printf("Error in generating private keys from the seed %s", err)
		panic(err)
	}

	rootPublicKey := rootPrivateKey.PublicKey()
	return rootPrivateKey, rootPublicKey
}

//GeneratePublicChildKey generates a child public key from the rootPublickey
func (instance *BipKeys) GeneratePublicChildKey(rootPublicKey *bip32.Key, childNumber uint32) (*bip32.Key, error) {
	key, err := rootPublicKey.NewChildKey(childNumber)
	if err != nil {
		log.Printf("There is an error in creating %s key from private key", childNumber)

	}

	return key, err

}

//GeneratePrivateChildKey generates a child private key from the rootPrivateKey
func (instance *BipKeys) GeneratePrivateChildKey(rootPrivateKey *bip32.Key, childNumber uint32) (*bip32.Key, *bip32.Key, error) {
	key, err := rootPrivateKey.NewChildKey(childNumber)
	if err != nil {
		log.Printf("There is an error in creating %s key from private key", childNumber)
	}
	return key, key.PublicKey(), err
}

//HexKeyEncoding Hex encoding of the keys
func (instance *BipKeys) HexKeyEncoding(extendedKey *bip32.Key) string {
	hexKey := hex.EncodeToString(extendedKey.Key)
	return hexKey
}

func generateMnemonic() string {
	var bipKeys BipKeys
	entropy, err := bipKeys.GenerateEntropy(128)
	if err != nil {
		log.Printf("Error in generating entropy", err)
	}

	mnemonic, _ := bipKeys.GenerateMnemonic(entropy)
	return mnemonic
}

//Given the mnemonic, returns zeroth index public and private key
func zerothKeys(mnemonic string, index uint32) (string, string) {
	var bipKeys BipKeys
	seed := bipKeys.GenerateSeed(mnemonic, []byte(""))
	rPublicKey, rPrivateKey := bipKeys.RootKeyGenerator(seed)
	// encodedRPublicKey := bipKeys.HexKeyEncoding(rPublicKey)
	// encodedRPrivateKey := bipKeys.HexKeyEncoding(rPrivateKey)

	// log.Printf(encodedRPrivateKey)
	// log.Printf(encodedRPublicKey)

	publicKey, _ := bipKeys.GeneratePublicChildKey(rPublicKey, index)
	privateKey, _ := bipKeys.GeneratePublicChildKey(rPrivateKey, index)
	encodedPubKey := bipKeys.HexKeyEncoding(publicKey)
	encodedPrivKey := bipKeys.HexKeyEncoding(privateKey)
	return encodedPubKey, encodedPrivKey

}

//Reponse Return
type Response struct {
	Mnemonic string `json:"mnemonic"`
	Public   string `json:"public"`
	Private  string `json:"private"`
}

//Request Request struct in which the lambda will receive its event
type Request struct {
	Mnemonic string `json:"mnemonic"`
	Index    uint32 `json:"key_index"`
}

//HandleLambdaEvent AWS lambda event handler
func HandleLambdaEvent(event Request) (Response, error) {
	if event.Mnemonic == "" {
		//Implies that we need to generate a new Mnemonic
		mnemonic := generateMnemonic()
		publickey, privatekey := zerothKeys(mnemonic, 0)
		return Response{Mnemonic: mnemonic, Public: publickey, Private: privatekey}, nil
	}

	publickey, privatekey := zerothKeys(event.Mnemonic, event.Index)
	return Response{Mnemonic: event.Mnemonic, Public: publickey, Private: privatekey}, nil
}

func main() {

	// mnemonic := generateMnemonic()
	// //var mnemonic = "orchard rule ring quiz lab amazing scene empower idle toddler private there list rate helmet thought wash cash pole bacon travel text evoke upon"
	// publickey, privatekey := zerothKeys(mnemonic, 0)
	// log.Printf(mnemonic)
	// log.Printf(publickey)
	// log.Printf(privatekey)
	lambda.Start(HandleLambdaEvent)
}
